#!/usr/bin/env bash
# Runs before each render. If python3 is not available, the data/_notes.yml
# file already in the repository is kept as is.
if command -v python3 >/dev/null 2>&1; then
  python3 "$(dirname "$0")/collect.py"
else
  echo "collect: python3 not found — English lists left unchanged"
fi
