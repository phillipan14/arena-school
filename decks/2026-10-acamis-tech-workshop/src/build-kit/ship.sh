#!/bin/bash
# Ship the Teacher Toolbox: commit only the build folder, push to main, and wait until it's live.
set -u
REPO="$(cd "$(dirname "$0")/../../../.." && pwd)"
B="talks/2026-10-acamis-tech-workshop/build"
URL="https://arenaschool.org/$B"
cd "$REPO" || exit 1
git add "$B"
git -c user.name="ACAMIS live build" -c user.email="jingjing@arenaschool.org" commit -q -m "ACAMIS live build: ${1:-update}" >/dev/null 2>&1 || echo "No new edits; pushing anything not yet published."
ok=0
for i in 1 2 3; do
  G="git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=10"
  $G pull -q --rebase --autostash origin main && $G push -q origin HEAD:main && { ok=1; break; }
  sleep 2
done
[ $ok = 1 ] || { echo "PUSH FAILED (no connection to GitHub). Check the VPN or hotspot, then run ./ship.sh again; the change is saved."; exit 1; }
want="$(git hash-object "$B/changes.txt")"
start=$(date +%s)
echo "Pushed. Waiting for the live site..."
while true; do
  got="$(curl -s -m 5 "$URL/changes.txt?t=$(date +%s)" | git hash-object --stdin)"
  [ "$got" = "$want" ] && { echo "LIVE after $(( $(date +%s) - start ))s: $URL"; exit 0; }
  [ $(( $(date +%s) - start )) -gt 180 ] && { echo "Pushed; still deploying. It should appear at $URL within a minute or two."; exit 0; }
  sleep 3
done
