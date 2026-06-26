#!/usr/bin/env bash
# portfolio_deploy_all.sh
# Drives the manual portfolio rollout for 7 repos.
# Pauses between repos so the user can do the web-dashboard steps (HF Space create, secret paste, Netlify env).
# Canonical env vars live in /Users/janelle/Documents/brain-university/PORTFOLIO_ENV.md

set -u

PORTFOLIO_ENV_FILE="/Users/janelle/Documents/brain-university/PORTFOLIO_ENV.md"

print_shared_secrets() {
  local space_name="$1"
  echo ""
  echo "--- Paste these 9 shared secrets into HF Space Settings -> Variables and secrets ---"
  if [ -f "$PORTFOLIO_ENV_FILE" ]; then
    echo "(canonical values: $PORTFOLIO_ENV_FILE)"
  else
    echo "(WARN: $PORTFOLIO_ENV_FILE missing — fill these in from your password manager)"
  fi
  cat <<'SECRETS'
  BU_AUTH_USER=
  BU_AUTH_PASSWORD=
  BU_AUTH_SECRET=
  BU_AUTH_TTL_HOURS=
  LLM_BACKEND=
  LOCAL_LLM_BASE=
  LOCAL_LLM_MODEL=
  LOCAL_LLM_KEY=
  ANTHROPIC_API_KEY=
SECRETS
  echo "  (per-project) CORS_ORIGINS=<frontend URL for $space_name>"
  echo "-------------------------------------------------------------------------------------"
  echo ""
}

push_repo() {
  local path="$1"
  if [ ! -d "$path" ]; then
    echo "  SKIP: $path does not exist on disk."
    return 1
  fi
  cd "$path" || return 1
  if git remote get-url origin >/dev/null 2>&1; then
    echo "  git push origin main"
    git push origin main
  else
    local name
    name="$(basename "$path")"
    echo "  No remote. Creating: gh repo create ghanemja/$name --private --source=. --push"
    gh repo create "ghanemja/$name" --private --source=. --push
  fi
}

pause_between() {
  echo ""
  read -r -p ">>> Finish the manual web-dashboard steps for this repo, then press [Enter] to continue... " _
  echo ""
}

############################################################
# 1. pptgpt — has-backend + has-frontend
############################################################
echo "=========================================="
echo "[1/7] pptgpt  (backend + frontend)"
echo "=========================================="
push_repo "/Users/janelle/Documents/pptgpt"
echo ""
echo "Now manually: huggingface.co/new-space -> jang0294/pptgpt Docker."
echo "Then: git remote add hf https://huggingface.co/spaces/jang0294/pptgpt && git push hf main"
print_shared_secrets "pptgpt"
echo "Frontend: netlify deploy --dir=netlify-dist --prod"
echo "(then set BU_API_BASE=https://jang0294-pptgpt.hf.space in Netlify env and redeploy)"
pause_between

############################################################
# 2. agentsannonymous — has-backend + has-frontend
############################################################
echo "=========================================="
echo "[2/7] agentsannonymous  (backend + frontend)"
echo "=========================================="
push_repo "/Users/janelle/Documents/agentsannonymous"
echo ""
echo "Now manually: huggingface.co/new-space -> jang0294/agentsannonymous Docker."
echo "Then: git remote add hf https://huggingface.co/spaces/jang0294/agentsannonymous && git push hf main"
print_shared_secrets "agentsannonymous"
echo "Frontend (optional mirror): netlify deploy --dir=design_system/ui_kits/run_and_view --prod"
echo "(then set BU_API_BASE=https://jang0294-agentsannonymous.hf.space in Netlify env)"
pause_between

############################################################
# 3. findme — does NOT exist on disk
############################################################
echo "=========================================="
echo "[3/7] findme  (SKIPPED — repo does not exist)"
echo "=========================================="
echo "  /Users/janelle/Documents/findme not found. Confirm name/path or scaffold first."
echo "  Existing siblings: agent-dashboard, agentsannonymous, bookshelf-portfolio,"
echo "  brain-university, charterscope(?), elms, ghanemja, ghanemja.github.io,"
echo "  inbox-zero-board(?), litreview, pptgpt, ..."
pause_between

############################################################
# 4. charterscope — has-backend + has-frontend (lives at /litreview)
############################################################
echo "=========================================="
echo "[4/7] charterscope  (backend + frontend, repo path: /litreview)"
echo "=========================================="
push_repo "/Users/janelle/Documents/litreview"
echo ""
echo "Now manually: huggingface.co/new-space -> jang0294/charterscope Docker."
echo "Then: git remote add hf https://huggingface.co/spaces/jang0294/charterscope && git push hf main"
print_shared_secrets "charterscope"
echo "Frontend: netlify deploy --dir=design --prod"
echo "(then set BU_API_BASE=https://jang0294-charterscope.hf.space in Netlify env)"
pause_between

############################################################
# 5. inbox-zero-board — static GH Pages only, no backend
############################################################
echo "=========================================="
echo "[5/7] inbox-zero-board  (static GH Pages, no backend)"
echo "=========================================="
push_repo "/Users/janelle/Documents/emails"
echo ""
echo "Now manually: GitHub repo Settings -> Pages -> Source: Deploy from a branch, main / (root)"
echo "Verify: https://ghanemja.github.io/inbox-zero-board/"
echo "(no HF Space, no secrets, no Netlify)"
pause_between

############################################################
# 6. bookshelf-portfolio — static, GH Pages via Actions (Netlify optional)
############################################################
echo "=========================================="
echo "[6/7] bookshelf-portfolio  (static, GH Actions deploy)"
echo "=========================================="
push_repo "/Users/janelle/Documents/bookshelf-portfolio"
echo ""
echo "Now manually: GitHub repo Settings -> Pages -> Source = 'GitHub Actions'"
echo "Live URL: https://ghanemja.github.io/bookshelf-portfolio/"
echo "Optional frontend mirror: netlify deploy --dir=. --prod"
pause_between

############################################################
# 7. ghanemja — profile README hub, already has remote
############################################################
echo "=========================================="
echo "[7/7] ghanemja  (profile README hub)"
echo "=========================================="
push_repo "/Users/janelle/Documents/ghanemja"
echo ""
echo "No HF Space, no Netlify. Just verify https://github.com/ghanemja shows updated README."
echo "After all other repos are live, come back and replace placeholder URLs in README.md."
echo ""

echo "=========================================="
echo "All 7 repos processed. Done."
echo "=========================================="
