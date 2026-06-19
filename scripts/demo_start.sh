#!/bin/bash
# Brain University — leadership demo launcher.
#
# Disables auth so leadership can poke around w/o a login screen, starts the
# FastAPI backend on :8090 + a static server on :8091 for the design/ folder,
# and opens the app in the default browser.
#
# Stop with Ctrl-C; both processes get killed via the EXIT trap.

set -euo pipefail

PORT_API=8090
PORT_STATIC=8091

cd "$(dirname "$0")/.."

# Kill anything still bound from a previous run
lsof -ti ":${PORT_API}" 2>/dev/null | xargs -r kill -9 2>/dev/null || true
lsof -ti ":${PORT_STATIC}" 2>/dev/null | xargs -r kill -9 2>/dev/null || true

echo "→ Launching backend on :${PORT_API} (auth disabled for demo)"
BU_AUTH_DISABLED=1 \
CORS_ORIGINS="http://localhost:${PORT_STATIC}" \
uvicorn api.server:app --port "${PORT_API}" --log-level warning &
API_PID=$!

echo "→ Launching static server on :${PORT_STATIC}"
( cd design && python3 -m http.server "${PORT_STATIC}" > /dev/null 2>&1 ) &
STATIC_PID=$!

cleanup() {
  echo
  echo "→ Stopping demo (pids $API_PID, $STATIC_PID)"
  kill $API_PID  2>/dev/null || true
  kill $STATIC_PID 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Wait a beat for processes to bind
sleep 2

URL="http://localhost:${PORT_STATIC}/Brain%20University.html"
echo "→ Opening ${URL}"
case "$(uname)" in
  Darwin*)  open    "${URL}" ;;
  Linux*)   xdg-open "${URL}" 2>/dev/null || true ;;
esac

echo
echo "Brain University running. Ctrl-C to stop."
echo "  backend : http://localhost:${PORT_API}/docs"
echo "  app     : ${URL}"
echo
echo "To re-enable auth for a public deploy, unset BU_AUTH_DISABLED and set:"
echo "  BU_AUTH_USER, BU_AUTH_PASSWORD, BU_AUTH_SECRET, CORS_ORIGINS"
echo

# Block until user kills us
wait $API_PID
