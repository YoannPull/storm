#!/usr/bin/env python3
# =============================================================================
#  Adresses propres — lancé par assemble.sh après chaque rendu.
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
import glob
import os
import re

SKIP = re.compile(r"^(https?:|mailto:|tel:|//|data:|javascript:|#)")
HREF = re.compile(r'(href=")([^"]*)(")')


def clean(match):
    url = match.group(2)
    if not url or SKIP.match(url):
        return match.group(0)
    cut = min([i for i in (url.find("#"), url.find("?")) if i >= 0], default=len(url))
    path, rest = url[:cut], url[cut:]
    if path.endswith("index.html"):
        path = path[: -len("index.html")] or "./"
    elif path.endswith(".html"):
        path = path[: -len(".html")]
    else:
        return match.group(0)
    return match.group(1) + path + rest + match.group(3)


edition = os.environ.get("PROF", "fr")
count = 0
for f in glob.glob(os.path.join("docs", edition, "**", "*.html"), recursive=True):
    text = open(f, encoding="utf-8").read()
    new = HREF.sub(clean, text)
    if new != text:
        open(f, "w", encoding="utf-8").write(new)
        count += 1
print("clean_urls: %d pages mises à jour dans docs/%s" % (count, edition))
