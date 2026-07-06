#!/usr/bin/env bash
# restore_db.sh — guarded restore of a backup_db.sh artifact.
#
# Phase 5 ops (docs/HARDENING.md). DESTRUCTIVE: replaces the database that
# DATABASE_URL (or BRAIN_DB fallback) points at. Refuses to run without the
# explicit --yes-i-know flag; there are no interactive prompts.
#
# Usage:
#   scripts/restore_db.sh --yes-i-know backups/atp-20260706-031700.dump
#   scripts/restore_db.sh --yes-i-know backups/atp-20260706-031700.sqlite3.gpg
#
#   *.dump[.gpg]     → pg_restore --clean --if-exists into DATABASE_URL
#                      (must be a postgres URL)
#   *.sqlite3[.gpg]  → replaces the sqlite file (current one is kept as
#                      <db>.pre-restore-<stamp>); stale -wal/-shm removed
#   *.gpg            → decrypted first (your gpg keyring must hold the
#                      BACKUP_GPG_RECIPIENT private key)
#
# If a matching atp-<stamp>.sha256 manifest sits next to the artifact, the
# artifact's hash is verified BEFORE anything is touched.
#
# Exit codes:
#   0  restored
#   1  usage / guard / configuration error (nothing touched)
#   2  integrity check failed (nothing touched)
#   3  restore step failed
#
# After a restore, verify the tamper-evident evidence chain per org — the
# hint is printed on success.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

log() { printf '[restore_db] %s\n' "$*" >&2; }
die() { printf '[restore_db] ERROR: %s\n' "$1" >&2; exit "${2:-1}"; }

usage() {
  cat >&2 <<'EOF'
Usage: scripts/restore_db.sh --yes-i-know <backup-artifact>

DESTRUCTIVE. Overwrites the database at DATABASE_URL (or the sqlite file at
BRAIN_DB / data/brain_university.db when DATABASE_URL is unset).
The --yes-i-know flag is REQUIRED; nothing runs without it.
EOF
  exit 1
}

# ── Args: --yes-i-know guard + artifact path (any order) ────────────────────
CONFIRMED=0
ARTIFACT=""
for arg in "$@"; do
  case "${arg}" in
    --yes-i-know) CONFIRMED=1 ;;
    -h|--help)    usage ;;
    -*)           die "unknown flag: ${arg}" 1 ;;
    *)            [ -z "${ARTIFACT}" ] || die "exactly one backup artifact, got extra: ${arg}" 1
                  ARTIFACT="${arg}" ;;
  esac
done
[ "${CONFIRMED}" = "1" ] || usage
[ -n "${ARTIFACT}" ] || usage
[ -f "${ARTIFACT}" ] || die "no such file: ${ARTIFACT}" 1
ARTIFACT="$(cd "$(dirname "${ARTIFACT}")" && pwd)/$(basename "${ARTIFACT}")"

# ── Resolve target database (same parse as backup_db.sh / atp/db.py) ────────
DB_KIND="" PG_URL="" SQLITE_PATH=""
url="${DATABASE_URL:-}"
case "${url}" in
  '' )
    DB_KIND="sqlite"
    SQLITE_PATH="${BRAIN_DB:-${REPO_ROOT}/data/brain_university.db}"
    ;;
  sqlite:///* )
    DB_KIND="sqlite"
    SQLITE_PATH="${url#sqlite:///}"
    [ "${SQLITE_PATH#/}" = "${SQLITE_PATH}" ] && SQLITE_PATH="${REPO_ROOT}/${SQLITE_PATH}"
    ;;
  postgres://* | postgresql://* | postgresql+psycopg2://* )
    DB_KIND="postgres"
    PG_URL="${url/postgresql+psycopg2:\/\//postgresql://}"
    PG_URL="${PG_URL/postgres:\/\//postgresql://}"
    ;;
  * )
    die "unsupported DATABASE_URL scheme: ${url%%://*}://…" 1
    ;;
esac

# ── Manifest check (when the backup run's .sha256 sits next to the file) ────
verify_against_manifest() {
  local dir base stem manifest sha
  dir="$(dirname "${ARTIFACT}")"
  base="$(basename "${ARTIFACT}")"
  stem="$(printf '%s' "${base}" | grep -oE '^atp-[0-9]{8}-[0-9]{6}' || true)"
  [ -n "${stem}" ] || { log "no atp-<stamp> stem — skipping manifest check"; return 0; }
  manifest="${dir}/${stem}.sha256"
  [ -f "${manifest}" ] || { log "no manifest ${stem}.sha256 — skipping integrity check"; return 0; }
  if command -v sha256sum >/dev/null 2>&1; then sha=(sha256sum)
  elif command -v shasum >/dev/null 2>&1; then sha=(shasum -a 256)
  else log "no sha256 tool — skipping integrity check"; return 0; fi
  ( cd "${dir}" && grep -F "  ${base}" "${manifest}" | "${sha[@]}" --check --status - ) \
    || die "sha256 mismatch for ${base} against ${stem}.sha256 — refusing to restore" 2
  log "integrity OK: ${base} matches ${stem}.sha256"
}
verify_against_manifest

# ── GPG decrypt when needed ──────────────────────────────────────────────────
CLEANUP=""
trap '[ -n "${CLEANUP}" ] && rm -f "${CLEANUP}"' EXIT
PLAIN="${ARTIFACT}"
if [ "${ARTIFACT%.gpg}" != "${ARTIFACT}" ]; then
  command -v gpg >/dev/null 2>&1 || die "artifact is .gpg but gpg not on PATH" 1
  PLAIN="$(mktemp "${TMPDIR:-/tmp}/restore_db.XXXXXX")"
  CLEANUP="${PLAIN}"
  log "decrypting $(basename "${ARTIFACT}")"
  gpg --batch --yes --quiet --output "${PLAIN}" --decrypt "${ARTIFACT}" \
    || die "gpg decrypt failed (is the BACKUP_GPG_RECIPIENT private key in this keyring?)" 3
fi

# ── Kind/target cross-check + restore ────────────────────────────────────────
BASE_NOGPG="$(basename "${ARTIFACT%.gpg}")"
STAMP="$(date -u +%Y%m%d-%H%M%S)"
case "${BASE_NOGPG}" in
  *.dump )
    [ "${DB_KIND}" = "postgres" ] \
      || die "${BASE_NOGPG} is a Postgres dump but DATABASE_URL is not postgres" 1
    command -v pg_restore >/dev/null 2>&1 || die "pg_restore not on PATH" 1
    log "pg_restore --clean --if-exists into ${PG_URL%%@*}@… (existing objects are dropped)"
    pg_restore --clean --if-exists --no-owner --exit-on-error \
      --dbname "${PG_URL}" "${PLAIN}" \
      || die "pg_restore failed — database may be partially restored" 3
    ;;
  *.sqlite3 )
    [ "${DB_KIND}" = "sqlite" ] \
      || die "${BASE_NOGPG} is a sqlite snapshot but DATABASE_URL is postgres" 1
    mkdir -p "$(dirname "${SQLITE_PATH}")"
    if [ -f "${SQLITE_PATH}" ]; then
      mv "${SQLITE_PATH}" "${SQLITE_PATH}.pre-restore-${STAMP}"
      log "current db kept at ${SQLITE_PATH}.pre-restore-${STAMP}"
    fi
    rm -f "${SQLITE_PATH}-wal" "${SQLITE_PATH}-shm" "${SQLITE_PATH}-journal"
    cp "${PLAIN}" "${SQLITE_PATH}" || die "copy into ${SQLITE_PATH} failed" 3
    log "restored sqlite db at ${SQLITE_PATH}"
    ;;
  * )
    die "unrecognized artifact type: ${BASE_NOGPG} (expect *.dump[.gpg] or *.sqlite3[.gpg])" 1
    ;;
esac

log "restore complete: ${BASE_NOGPG}"
cat >&2 <<'EOF'
[restore_db] NEXT — verify the tamper-evident evidence chain PER ORG
[restore_db] (needs the production EVIDENCE_SIGNING_KEY in the environment):
[restore_db]
[restore_db]   python3 -c "from atp import signing; import json; \
[restore_db]     print(json.dumps(signing.verify_chain('org-demo')))"
[restore_db]
[restore_db] Expect {"ok": true, ...} for every org id in the orgs table.
[restore_db] (`python3 -m atp.exams <cert> --dry-run --verify-chain --org <org>`
[restore_db]  also verifies, but only AFTER running a fresh exam — use the
[restore_db]  one-liner above for a pure post-restore check.)
EOF
