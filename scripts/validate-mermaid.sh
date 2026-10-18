#!/bin/sh
# Uso: sh scripts/validate-mermaid.sh archivo.mmd
# Valida la sintaxis renderizando con mermaid-cli (mmdc). Si no está instalado, lo indica.
set -u
[ $# -eq 1 ] || { echo "Uso: $0 archivo.mmd"; exit 2; }
[ -f "$1" ] || { echo "No existe: $1"; exit 2; }

if ! command -v mmdc >/dev/null 2>&1; then
  echo "NO VALIDADO: mmdc no está instalado (npm i -g @mermaid-js/mermaid-cli)"
  exit 3
fi

out="$(mktemp -t mermaid-XXXXXX).svg"
if mmdc -i "$1" -o "$out" >/dev/null 2>&1; then
  echo "VALIDADO: $1"
  rm -f "$out"
else
  echo "ERROR de sintaxis en $1"
  rm -f "$out"
  exit 1
fi
