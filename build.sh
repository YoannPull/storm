#!/usr/bin/env bash
# =============================================================================
#  Builds both editions into docs/
#
#      bash build.sh
#
#  Equivalent to:
#      quarto render                 (French edition)
#      quarto render --profile en    (English edition)
#
#  Each render copies itself into docs/ (see scripts/assemble.sh).
# =============================================================================
set -e
cd "$(dirname "$0")"

# Intermediate render folders (not tracked by git): start from scratch on every
# build, since docs/ is rebuilt from them.
rm -rf _site-fr _site-en

quarto render
quarto render --profile en

echo
echo "✓ site built in docs/  →  local preview: python3 -m http.server -d docs  then http://localhost:8000"
