#!/usr/bin/env python3
# =============================================================================
#  Extrait les en-têtes des notes françaises vers data/_notes.yml.
#
#  Pourquoi : Quarto ne sait lire les en-têtes que des fichiers qu'il rend.
#  L'édition anglaise ne rend pas les pages françaises — sans ce script, ses
#  listes sortiraient vides. Le script relit donc fr/notes/*.qmd et écrit
#  un fichier que les deux éditions lisent (accueil, Actualités / News).
#
#  Lancé automatiquement avant chaque rendu (clé pre-render de _quarto.yml).
#  Le fichier produit (data/_notes.yml) ne se modifie
#  jamais à la main : il est réécrit à chaque construction.
# =============================================================================

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def front_matter(path):
    """Lit l'en-tête YAML d'un .qmd. Gère les scalaires, les listes en ligne
    ([a, b]) et les listes en bloc (- a). Suffisant pour nos en-têtes."""
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    data, key = {}, None
    for raw in m.group(1).split("\n"):
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.match(r"^\s+-\s+", line) and key:                 # liste en bloc
            if not isinstance(data.get(key), list):
                data[key] = []                                  # la clé était vide
            data[key].append(re.sub(r"^\s+-\s+", "", line).strip().strip('"\''))
            continue
        km = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if not km:
            continue
        key, val = km.group(1), km.group(2)
        val = re.sub(r"\s+#.*$", "", val).strip()               # commentaire de fin
        if val.startswith("[") and val.endswith("]"):
            items = [v.strip().strip('"\'') for v in val[1:-1].split(",")]
            data[key] = [v for v in items if v]
        elif val in ("", ">-", "|", ">"):
            data[key] = ""
        else:
            data[key] = val.strip().strip('"\'')
    return data


def q(v):
    """Échappe une valeur pour du YAML entre guillemets."""
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def write(dest, rows, header):
    lines = [header, ""]
    for r in rows:
        first = True
        for k, v in r.items():
            prefix = "- " if first else "  "
            first = False
            if isinstance(v, list):
                lines.append(prefix + k + ": [" + ", ".join(q(x) for x in v) + "]")
            else:
                lines.append(prefix + k + ": " + q(v))
        lines.append("")
    open(os.path.join(ROOT, dest), "w", encoding="utf-8").write("\n".join(lines))
    print("collect: %s (%d entrées)" % (dest, len(rows)))


HEADER = ("# Fichier produit automatiquement par scripts/collect.py.\n"
          "# Ne pas modifier à la main : il est réécrit à chaque construction.")

# --- Notes -------------------------------------------------------------------
notes = []
for f in sorted(glob.glob(os.path.join(ROOT, "fr/notes/*.qmd"))):
    if os.path.basename(f) == "index.qmd":
        continue
    fm = front_matter(f)
    if not fm.get("title"):
        continue
    slug = os.path.splitext(os.path.basename(f))[0]
    auteurs = fm.get("author", [])
    if isinstance(auteurs, str):
        auteurs = [auteurs] if auteurs else []
    notes.append({
        "title": fm["title"],
        "path": "/fr/notes/%s.html" % slug,
        "date": fm.get("date", ""),
        "auteurs": auteurs,
        "description": fm.get("description", ""),
        "categories": fm.get("categories", []),
    })
notes.sort(key=lambda r: r["date"], reverse=True)
write("data/_notes.yml", notes, HEADER)
