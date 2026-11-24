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
#
#  Ajoute aussi, dans chaque page, les balises de partage que Quarto ne met
#  pas (LinkedIn, X, Slack…) : og:url et lien canonique (adresse propre),
#  og:type, og:locale, taille de l'image de partage, liens vers l'autre langue,
#  et un twitter:title aligné sur og:title.
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


# Pages équivalentes dans les deux langues (liens hreflang)
PAIRS = {"fr/": "en/", "fr/expertise/": "en/expertise/", "fr/actualites/": "en/news/",
         "fr/publications/": "en/publications/", "fr/a-propos/": "en/about/", "fr/notes/": "en/notes/"}
PAIRS.update({v: k for k, v in PAIRS.items()})
OG_TITLE = re.compile(r'<meta property="og:title" content="([^"]*)"\s*/?>')
TW_TITLE = re.compile(r'<meta name="twitter:title" content="[^"]*"\s*/?>')


def share_tags(page, docs, origin):
    """Balises de partage d'une page (idempotent : rien si og:url existe déjà)."""
    text = page.read_text(encoding="utf-8")
    if 'property="og:url"' in text or "</head>" not in text:
        return False
    rel = clean_path(page.relative_to(docs).as_posix())
    url = f"{origin}/{quote(rel)}"
    lang = rel.split("/")[0]
    tags = [f'<link rel="canonical" href="{url}">'] if 'rel="canonical"' not in text else []
    tags += [f'<meta property="og:url" content="{url}">',
             f'<meta property="og:type" content="{"article" if "/notes/" in rel and not rel.endswith("notes/") else "website"}">',
             f'<meta property="og:locale" content="{"fr_FR" if lang == "fr" else "en_GB"}">']
    if "og-storm-" in text:
        tags += ['<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">']
    if rel in PAIRS:
        other = PAIRS[rel]
        tags += [f'<link rel="alternate" hreflang="{lang}" href="{url}">',
                 f'<link rel="alternate" hreflang="{other.split("/")[0]}" href="{origin}/{other}">']
    m = OG_TITLE.search(text)
    if m:
        text = TW_TITLE.sub(f'<meta name="twitter:title" content="{m.group(1)}">', text)
    text = text.replace("</head>", "\n".join(tags) + "\n</head>", 1)
    page.write_text(text, encoding="utf-8")
    return True


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
origin = "https://" + (docs / "CNAME").read_text(encoding="utf-8").strip()
shared = sum(share_tags(page, docs, origin) for page in (docs / edition).rglob("*.html") if "/assets/" not in page.as_posix())
print("clean_urls: balises de partage ajoutées à %d pages" % shared)
write_sitemap(docs)
