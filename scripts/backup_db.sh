#!/usr/bin/env bash
# backup_db.sh — DATABASE_URL-aware backup with audit-surface CSV export.
#
# Phase 5 ops (docs/HARDENING.md). Cron-ready: no prompts, meaningful exit
# codes, absolute paths derived from this script's location.
#
#   DATABASE_URL unset / sqlite:///…  → sqlite3 .backup snapshot
#   DATABASE_URL postgres…            → pg_dump --format=custom
#
# Every run additionally exports the audit surfaces (docs/TENANCY.md) as CSV:
#   atp_evidence, atp_hitl, access_log, usage_events
# and writes a sha256 manifest which is verified before the script exits 0.
#
# Env knobs:
#   DATABASE_URL          same value the app uses (postgres://… is fine;
#                         the +psycopg2 driver suffix is stripped for pg_dump)
#   BRAIN_DB              sqlite path when DATABASE_URL is unset
#                         (default: <repo>/data/brain_university.db)
#   BACKUP_DIR            output directory (default: <repo>/backups)
#   BACKUP_KEEP           retention — keep this many newest runs (default: 14)
#   BACKUP_GPG_RECIPIENT  when set, every artifact is GPG-encrypted to this
#                         recipient and the plaintext removed (leak-surface
#                         #7 in docs/TENANCY.md: backups must not leak T2).
#                         The manifest hashes the ciphertext, so integrity
#                         checks never require the private key.
#
# Exit codes:
#   0  backup written, manifest verified, retention pruned
#   1  configuration / missing-tool error (nothing written)
#   2  dump or export step failed
#   3  manifest verification failed (artifacts are suspect — do not trust)
#
# Postgres + RLS note: the ATP tables are FORCE ROW LEVEL SECURITY
# (migrations 005/006). This script sets row_security=off for the CSV
# exports, and pg_dump does the same by default — so a role WITHOUT
# BYPASSRLS fails LOUDLY instead of silently exporting 0 rows. Run backups
# as a superuser or a dedicated role with BYPASSRLS.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BACKUP_DIR="${BACKUP_DIR:-${REPO_ROOT}/backups}"
BACKUP_KEEP="${BACKUP_KEEP:-14}"
GPG_RECIPIENT="${BACKUP_GPG_RECIPIENT:-}"

# Audit surfaces (docs/TENANCY.md) exported as CSV on every run.
AUDIT_TABLES=(atp_evidence atp_hitl access_log usage_events)

STAMP="$(date -u +%Y%m%d-%H%M%S)"
STEM="atp-${STAMP}"

log()  { printf '[backup_db] %s\n' "$*" >&2; }
die()  { printf '[backup_db] ERROR: %s\n' "$1" >&2; exit "${2:-1}"; }

case "${BACKUP_KEEP}" in
  ''|*[!0-9]*) die "BACKUP_KEEP must be a non-negative integer (got '${BACKUP_KEEP}')" 1 ;;
esac

# sha256 tool: GNU coreutils on Linux, shasum on stock macOS.
if command -v sha256sum >/dev/null 2>&1; then
  SHA=(sha256sum)
elif command -v shasum >/dev/null 2>&1; then
  SHA=(shasum -a 256)
else
  die "need sha256sum or shasum on PATH" 1
fi

# ── Resolve the database from DATABASE_URL (mirror atp/db.py) ───────────────
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
    # sqlite:////abs/path keeps its leading slash after stripping; a
    # relative path is resolved against the repo root (app runs from there).
    [ "${SQLITE_PATH#/}" = "${SQLITE_PATH}" ] && SQLITE_PATH="${REPO_ROOT}/${SQLITE_PATH}"
    ;;
  postgres://* | postgresql://* | postgresql+psycopg2://* )
    DB_KIND="postgres"
    # pg_dump/psql want a plain postgresql:// URL — strip driver suffixes.
    PG_URL="${url/postgresql+psycopg2:\/\//postgresql://}"
    PG_URL="${PG_URL/postgres:\/\//postgresql://}"
    ;;
  * )
    die "unsupported DATABASE_URL scheme: ${url%%://*}://…" 1
    ;;
esac

if [ "${DB_KIND}" = "sqlite" ]; then
  command -v sqlite3 >/dev/null 2>&1 || die "sqlite3 not on PATH" 1
  [ -f "${SQLITE_PATH}" ] || die "sqlite database not found: ${SQLITE_PATH}" 1
else
  command -v pg_dump >/dev/null 2>&1 || die "pg_dump not on PATH (install postgresql client tools)" 1
  command -v psql    >/dev/null 2>&1 || die "psql not on PATH (needed for CSV export)" 1
fi
if [ -n "${GPG_RECIPIENT}" ]; then
  command -v gpg >/dev/null 2>&1 || die "BACKUP_GPG_RECIPIENT set but gpg not on PATH" 1
fi

mkdir -p "${BACKUP_DIR}"
# Backups must never be committed (leak-surface #7) — self-ignore the dir.
[ -f "${BACKUP_DIR}/.gitignore" ] || printf '*\n' > "${BACKUP_DIR}/.gitignore"

ARTIFACTS=()  # basenames, relative to BACKUP_DIR

# ── 1. Full database snapshot ────────────────────────────────────────────────
if [ "${DB_KIND}" = "sqlite" ]; then
  SNAP="${STEM}.sqlite3"
  log "sqlite .backup ${SQLITE_PATH} -> ${SNAP}"
  sqlite3 "${SQLITE_PATH}" ".backup '${BACKUP_DIR}/${SNAP}'" \
    || die "sqlite3 .backup failed" 2
  ARTIFACTS+=("${SNAP}")
else
  SNAP="${STEM}.dump"
  log "pg_dump (custom format) -> ${SNAP}"
  pg_dump --format=custom --no-owner --file "${BACKUP_DIR}/${SNAP}" "${PG_URL}" \
    || die "pg_dump failed (a non-BYPASSRLS role errors on FORCE RLS tables — see header)" 2
  ARTIFACTS+=("${SNAP}")
fi

# ── 2. CSV export of the audit surfaces ──────────────────────────────────────
for t in "${AUDIT_TABLES[@]}"; do
  CSV="${STEM}.${t}.csv"
  if [ "${DB_KIND}" = "sqlite" ]; then
    exists="$(sqlite3 -readonly "${SQLITE_PATH}" \
      "SELECT 1 FROM sqlite_master WHERE type='table' AND name='${t}' LIMIT 1;")"
    if [ -z "${exists}" ]; then
      log "WARN: table ${t} not present (migration not applied yet) — skipping"
      continue
    fi
    sqlite3 -readonly "${SQLITE_PATH}" \
      ".headers on" ".mode csv" "SELECT * FROM ${t};" \
      > "${BACKUP_DIR}/${CSV}" || die "CSV export of ${t} failed" 2
    # sqlite3 emits nothing for an empty result set — still write the header
    # row so empty exports match the Postgres \copy HEADER shape.
    if [ ! -s "${BACKUP_DIR}/${CSV}" ]; then
      sqlite3 -readonly "${SQLITE_PATH}" \
        "SELECT group_concat(name, ',') FROM pragma_table_info('${t}');" \
        > "${BACKUP_DIR}/${CSV}" || die "CSV header export of ${t} failed" 2
    fi
  else
    exists="$(psql "${PG_URL}" -qAt -v ON_ERROR_STOP=1 \
      -c "SELECT COALESCE(to_regclass('public.${t}')::text, '')" )" \
      || die "table check for ${t} failed" 2
    if [ -z "${exists}" ]; then
      log "WARN: table ${t} not present (migration not applied yet) — skipping"
      continue
    fi
    # row_security=off: fail loudly if this role cannot bypass FORCE RLS,
    # instead of exporting an empty (org-filtered) CSV.
    psql "${PG_URL}" -q -v ON_ERROR_STOP=1 \
      -c "SET row_security = off" \
      -c "\\copy (SELECT * FROM ${t}) TO '${BACKUP_DIR}/${CSV}' WITH (FORMAT csv, HEADER)" \
      || die "CSV export of ${t} failed (BYPASSRLS role required — see header)" 2
  fi
  rows=$(( $(wc -l < "${BACKUP_DIR}/${CSV}") - 1 ))
  [ "${rows}" -lt 0 ] && rows=0
  log "exported ${t}: ${rows} row(s) -> ${CSV}"
  ARTIFACTS+=("${CSV}")
done

# ── 3. Optional GPG encryption (leak-surface #7) ─────────────────────────────
if [ -n "${GPG_RECIPIENT}" ]; then
  ENC=()
  for f in "${ARTIFACTS[@]}"; do
    if ! gpg --batch --yes --trust-model always \
             --recipient "${GPG_RECIPIENT}" \
             --output "${BACKUP_DIR}/${f}.gpg" --encrypt "${BACKUP_DIR}/${f}"; then
      # Never leave plaintext behind when encryption was requested (#7):
      # scrap the whole run so cron alerts and nothing sensitive lingers.
      rm -f "${BACKUP_DIR}/${STEM}."*
      die "gpg encrypt of ${f} failed — run ${STEM} removed" 2
    fi
    rm -f "${BACKUP_DIR}/${f}"
    ENC+=("${f}.gpg")
  done
  ARTIFACTS=("${ENC[@]}")
  log "encrypted ${#ARTIFACTS[@]} artifact(s) to ${GPG_RECIPIENT}"
fi

# ── 4. sha256 manifest + verification ────────────────────────────────────────
MANIFEST="${STEM}.sha256"
( cd "${BACKUP_DIR}" && "${SHA[@]}" "${ARTIFACTS[@]}" > "${MANIFEST}" ) \
  || die "manifest write failed" 2
( cd "${BACKUP_DIR}" && "${SHA[@]}" --check --status "${MANIFEST}" ) \
  || die "manifest verification FAILED for ${STEM} — artifacts are suspect" 3
log "manifest verified: ${MANIFEST}"

# ── 5. Retention prune: keep the newest BACKUP_KEEP runs ─────────────────────
# A "run" is every file sharing an atp-YYYYmmdd-HHMMSS stem; the stamp sorts
# lexicographically = chronologically. Only stem-matching files are touched.
if [ "${BACKUP_KEEP}" -gt 0 ]; then
  stems="$(find "${BACKUP_DIR}" -maxdepth 1 -name 'atp-*' \
             | grep -oE 'atp-[0-9]{8}-[0-9]{6}' | sort -u || true)"
  total="$(printf '%s\n' "${stems}" | grep -c . || true)"
  if [ "${total}" -gt "${BACKUP_KEEP}" ]; then
    printf '%s\n' "${stems}" | head -n "$(( total - BACKUP_KEEP ))" \
      | while IFS= read -r stem; do
          [ -n "${stem}" ] || continue
          log "prune: removing run ${stem}"
          find "${BACKUP_DIR}" -maxdepth 1 -name "${stem}.*" -delete
        done
  fi
fi

log "OK ${STEM} (${#ARTIFACTS[@]} artifact(s) + manifest) in ${BACKUP_DIR}"
