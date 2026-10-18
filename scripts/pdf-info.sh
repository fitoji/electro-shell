#!/bin/sh
# Uso: sh scripts/pdf-info.sh archivo.pdf
# Inventario rápido: páginas, metadatos y si el PDF tiene texto seleccionable.
set -u
[ $# -eq 1 ] || { echo "Uso: $0 archivo.pdf"; exit 2; }
[ -f "$1" ] || { echo "No existe: $1"; exit 2; }

# Python del venv del proyecto si existe (ahí están pypdf y demás dependencias)
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PY="$DIR/../.venv/bin/python"
[ -x "$PY" ] || PY=python3

"$PY" -I - "$1" <<'PY'
import sys
from pypdf import PdfReader
r = PdfReader(sys.argv[1])
n = len(r.pages)
print(f"Páginas: {n}")
meta = r.metadata or {}
for k in ("/Title", "/Author", "/Producer", "/CreationDate"):
    if meta.get(k):
        print(f"{k[1:]}: {meta.get(k)}")
sample = list(range(min(n, 5)))
with_text = sum(1 for i in sample if (r.pages[i].extract_text() or "").strip())
print(f"Páginas con texto (de las {len(sample)} primeras): {with_text}")
if with_text == 0:
    print("AVISO: parece un PDF escaneado; no hay texto seleccionable.")
if r.is_encrypted:
    print("AVISO: el PDF está cifrado.")
PY
