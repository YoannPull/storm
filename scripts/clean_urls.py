#!/usr/bin/env python3
# =============================================================================
#  Adresses propres et plan du site — lancé par assemble.sh après chaque rendu.
#
#  Dans les pages copiées dans docs/<édition>/, les liens internes perdent
#  « index.html » et « .html » :
#      ../fr/expertise/index.html   →  ../fr/expertise/
#      ../notes/downscaling.html    →  ../notes/downscaling
#  GitHub Pages sert ces adresses tout seul. Les liens externes (http…),
#  mailto: et les ancres seules (#…) ne sont pas touchés.
#
#  Conséquence : ouvrir docs/fr/index.html directement depuis le disque ne
#  permet plus de naviguer de page en page. Pour un aperçu local, utiliser
#  « quarto preview », ou servir le dossier : python3 -m http.server -d docs
# =============================================================================
import os
import re
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape

SKIP = re.compile(r"^(https?:|mailto:|tel:|//|data:|javascript:|#)")
HREF = re.compile(r'(href=")([^"]*)(")')


def clean_path(path):
    if path == "index.html" or path.endswith("/index.html"):
        return path[: -len("index.html")] or "./"
    if path.endswith(".html"):
        return path[: -len(".html")]
    return path


def clean(match):
    url = match.group(2)
    if not url or SKIP.match(url):
        return match.group(0)
    cut = min([i for i in (url.find("#"), url.find("?")) if i >= 0], default=len(url))
    path, rest = url[:cut], url[cut:]
    return match.group(1) + clean_path(path) + rest + match.group(3)


def write_sitemap(docs):
    origin = "https://" + (docs / "CNAME").read_text(encoding="utf-8").strip()
    paths = sorted(
        clean_path(page.relative_to(docs).as_posix())
        for language in ("fr", "en")
        for page in (docs / language).rglob("*.html")
    )
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in paths:
        url = escape(f"{origin}/{quote(path)}")
        lines.extend(["  <url>", f"    <loc>{url}</loc>", "  </url>"])
    lines.append("</urlset>")
    (docs / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (docs / "robots.txt").write_text(f"Sitemap: {origin}/sitemap.xml\n", encoding="utf-8")


docs = Path("docs")
edition = os.environ.get("PROF", "fr")
count = 0
for page in (docs / edition).rglob("*.html"):
    text = page.read_text(encoding="utf-8")
    new = HREF.sub(clean, text)
    if new != text:
        page.write_text(new, encoding="utf-8")
        count += 1
print("clean_urls: %d pages mises à jour dans docs/%s" % (count, edition))
write_sitemap(docs)
