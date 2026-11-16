#!/usr/bin/env bash
# =============================================================================
#  Construit les deux éditions dans docs/
#
#      bash build.sh
#
#  Équivaut à :
#      quarto render                 (édition française)
#      quarto render --profile en    (édition anglaise)
#
#  Chaque rendu se recopie tout seul dans docs/ (voir scripts/assemble.sh).
# =============================================================================
set -e
cd "$(dirname "$0")"

quarto render
quarto render --profile en

echo
echo "✓ site construit dans docs/  →  ouvrir docs/fr/index.html"
