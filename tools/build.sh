#!/bin/sh
# Build every page from its sources, in order; with --check, lint only (exit 1 on any drift or failure).
# The site header and footer come from partials/ (tools/site_nav.py) before anything else touches the pages.
#   sh tools/build.sh           write
#   sh tools/build.sh --check   lint: nav/footer identical to partials, generated parts converged, links, content
set -e
cd "$(dirname "$0")/.."
if [ "$1" = "--check" ]; then
  python3 tools/site_nav.py --check
  python3 tools/site_nav.py --report | tail -1
  for t in hero_markup pro_markup phone_markup approach_page past_talks data_section; do
    r=$(python3 tools/$t.py --check | tail -1); echo "$t: $r"
    echo "$r" | grep -q "Would change 0" || { echo "FAIL: $t not converged"; exit 1; }
  done
  python3 tools/link_check.py | tail -1 | tee /dev/stderr | grep -q " 0 broken"
  python3 tools/content_lint.py >/dev/null
  echo "build check: ok"
else
  python3 tools/site_nav.py
  python3 tools/past_talks.py | tail -1
  python3 tools/data_section.py | tail -1
  python3 tools/hero_markup.py | tail -1
  python3 tools/phone_build.py | tail -1
  python3 tools/phone_markup.py | tail -1
  python3 tools/newsletter_markup.py | tail -1
  python3 tools/pro_markup.py | tail -1
fi
