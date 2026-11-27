#!/usr/bin/env bash
# =============================================================================
#  Run automatically by Quarto after each render (post-render key).
#  Copies the edition that was just built into docs/.
#  You should never need to run this script by hand.
# =============================================================================
set -e

PROF="${QUARTO_PROFILE:-fr}"
OUT="${QUARTO_PROJECT_OUTPUT_DIR:-_site-$PROF}"

[ -d "$OUT/$PROF" ] || { echo "assemble: nothing to copy from $OUT/$PROF"; exit 0; }

mkdir -p docs
# GitHub Pages: disable Jekyll (otherwise some files may be ignored)
touch docs/.nojekyll
# Custom domain (GitHub Pages) — keep in sync with Settings → Pages
echo "squaremanagement-storm.com" > docs/CNAME
# Tab icon at the root (some browsers always ask for it there)
[ -f assets/brand/favicon.ico ] && cp assets/brand/favicon.ico docs/favicon.ico
# "Page not found" page (GitHub Pages serves it for any unknown address)
[ -f scripts/404.html ] && cp scripts/404.html docs/404.html
rm -rf "docs/$PROF"
cp -R "$OUT/$PROF" "docs/$PROF"

[ -d "$OUT/assets" ] && { rm -rf docs/assets; cp -R "$OUT/assets" docs/assets; }
mkdir -p docs/site_libs
[ -d "$OUT/site_libs" ] && cp -R "$OUT/site_libs/." docs/site_libs/

# Search index: one per edition, merged into a single one for the whole site.
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

# Clean URLs: internal links no longer show "index.html" or ".html"
# (GitHub Pages serves /fr/expertise/ and /fr/notes/downscaling on its own).
# The sitemap uses these addresses for both editions present in docs/.
if command -v python3 >/dev/null 2>&1; then
  PROF="$PROF" python3 scripts/clean_urls.py
else
  echo "assemble: python3 not found — sitemap not regenerated"
fi

# Root page: redirects to the French edition (its text stays in French,
# since visitors may briefly see it).
cat > docs/index.html <<'HTML'
<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<title>STORM — Quantitative Risk Collective</title>
<meta name="description" content="STORM, un collectif de recherche quantitative de Square Management.">
<meta property="og:title" content="STORM — Quantitative Risk Collective">
<meta property="og:description" content="Un collectif de recherche quantitative de Square Management.">
<meta property="og:url" content="https://squaremanagement-storm.com/">
<meta property="og:image" content="https://squaremanagement-storm.com/assets/brand/og-storm-fr.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://squaremanagement-storm.com/assets/brand/og-storm-fr.png">
<link rel="icon" href="favicon.ico">
<link rel="canonical" href="https://squaremanagement-storm.com/fr/">
<meta http-equiv="refresh" content="0; url=fr/">
</head><body><p>Redirection vers <a href="fr/">STORM</a>…</p></body></html>
HTML

echo "assemble: $PROF edition copied into docs/$PROF"
