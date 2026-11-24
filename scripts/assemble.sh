#!/usr/bin/env bash
# =============================================================================
#  Exécuté automatiquement par Quarto après chaque rendu (clé post-render).
#  Recopie l'édition qui vient d'être construite dans docs/.
#  Vous n'avez normalement jamais à lancer ce script à la main.
# =============================================================================
set -e

PROF="${QUARTO_PROFILE:-fr}"
OUT="${QUARTO_PROJECT_OUTPUT_DIR:-_site-$PROF}"

[ -d "$OUT/$PROF" ] || { echo "assemble: rien à copier depuis $OUT/$PROF"; exit 0; }

mkdir -p docs
# GitHub Pages : désactive Jekyll (sinon certains fichiers peuvent être ignorés)
touch docs/.nojekyll
# Domaine personnalisé (GitHub Pages) — à garder en phase avec Settings → Pages
echo "squaremanagement-storm.com" > docs/CNAME
# Icône d’onglet à la racine (certains navigateurs la demandent toujours là)
[ -f assets/brand/favicon.ico ] && cp assets/brand/favicon.ico docs/favicon.ico
rm -rf "docs/$PROF"
cp -R "$OUT/$PROF" "docs/$PROF"

[ -d "$OUT/assets" ] && { rm -rf docs/assets; cp -R "$OUT/assets" docs/assets; }
mkdir -p docs/site_libs
[ -d "$OUT/site_libs" ] && cp -R "$OUT/site_libs/." docs/site_libs/

# Index de recherche : un par édition, fusionnés en un seul pour tout le site.
if [ -f "$OUT/search.json" ]; then
  cp "$OUT/search.json" "docs/search-$PROF.json"
  if command -v python3 >/dev/null 2>&1; then
    python3 - <<'PY'
import glob, json, os
items = []
for f in sorted(glob.glob("docs/search-*.json")):
    try:
        items += json.load(open(f, encoding="utf-8"))
    except Exception:
        pass
if items:
    json.dump(items, open("docs/search.json", "w", encoding="utf-8"), ensure_ascii=False)
PY
  else
    cp "$OUT/search.json" docs/search.json
  fi
fi

# Adresses propres : les liens internes ne montrent plus « index.html » ni
# « .html » (GitHub Pages sert /fr/expertise/ et /fr/notes/downscaling tout seul).
# Le plan du site reprend ces adresses pour les deux éditions présentes dans docs/.
if command -v python3 >/dev/null 2>&1; then
  PROF="$PROF" python3 scripts/clean_urls.py
else
  echo "assemble: python3 absent — plan du site non régénéré"
fi

cat > docs/index.html <<'HTML'
<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<title>STORM — Quantitative Risk Collective</title>
<link rel="canonical" href="fr/">
<meta http-equiv="refresh" content="0; url=fr/">
</head><body><p>Redirection vers <a href="fr/">STORM</a>…</p></body></html>
HTML

echo "assemble: édition $PROF copiée dans docs/$PROF"
