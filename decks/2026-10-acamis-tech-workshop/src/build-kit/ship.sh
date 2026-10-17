#!/bin/bash
# Ship the Teacher Toolbox: commit only the build folder, push to main, and wait until it's live.
set -u
REPO="$(cd "$(dirname "$0")/../../../.." && pwd)"
B="talks/2026-10-acamis-tech-workshop/build"
URL="https://arenaschool.org/$B"
cd "$REPO" || exit 1
git add "$B"
git -c user.name="ACAMIS live build" -c user.email="jingjing@arenaschool.org" commit -q -m "ACAMIS live build: ${1:-update}" || { echo "Nothing new to ship."; exit 0; }
ok=0
for i in 1 2 3; do
  git pull -q --rebase --autostash origin main && git push -q origin HEAD:main && { ok=1; break; }
  sleep 2
done
[ $ok = 1 ] || { echo "PUSH FAILED: check the network, then run ./ship.sh again."; exit 1; }
want="$(git hash-object "$B/changes.txt")"
start=$(date +%s)
echo "Pushed. Waiting for the live site..."
while true; do
  got="$(curl -s -m 5 "$URL/changes.txt?t=$(date +%s)" | git hash-object --stdin)"
  [ "$got" = "$want" ] && { echo "LIVE after $(( $(date +%s) - start ))s: $URL"; exit 0; }
  [ $(( $(date +%s) - start )) -gt 180 ] && { echo "Pushed; still deploying. It should appear at $URL within a minute or two."; exit 0; }
  sleep 3
done
