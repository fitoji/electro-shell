#!/bin/sh
# Uso: sh scripts/recalc-xlsx.sh archivo.xlsx
# Recalcula las fórmulas con LibreOffice (headless) sobre una copia temporal y
# lista las celdas con errores. No modifica el archivo original.
set -u
[ $# -eq 1 ] || { echo "Uso: $0 archivo.xlsx"; exit 2; }
[ -f "$1" ] || { echo "No existe: $1"; exit 2; }

soffice_bin="$(command -v soffice || command -v libreoffice || true)"
[ -n "$soffice_bin" ] || { echo "NO COMPROBADO: LibreOffice no está instalado"; exit 3; }

tmp="$(mktemp -d)"
cp "$1" "$tmp/in.xlsx"
"$soffice_bin" --headless --convert-to xlsx:"Calc MS Excel 2007 XML" --outdir "$tmp/out" "$tmp/in.xlsx" >/dev/null 2>&1 \
  || { echo "ERROR: LibreOffice no pudo recalcular"; rm -rf "$tmp"; exit 1; }

python3 -I - "$tmp/out/in.xlsx" <<'PY'
import sys
from openpyxl import load_workbook
wb = load_workbook(sys.argv[1], data_only=True)
errors, formulas = [], 0
for ws in wb:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("#"):
                errors.append(f"{ws.title}!{c.coordinate}: {c.value}")
if errors:
    print("ERRORES:"); print("\n".join(errors)); sys.exit(1)
print("OK: sin errores de fórmula tras recalcular")
PY
status=$?
rm -rf "$tmp"
exit $status
