#!/usr/bin/env bash
# Lancé avant chaque rendu. Si python3 n'est pas disponible, on garde le
# fichier data/_notes.yml déjà présent dans le dépôt.
if command -v python3 >/dev/null 2>&1; then
  python3 "$(dirname "$0")/collect.py"
else
  echo "collect: python3 absent — listes anglaises inchangées"
fi
