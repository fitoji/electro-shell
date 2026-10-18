#!/bin/sh
# Valida frontmatter y orden de secciones de cada skills/*/SKILL.md
set -u
root="$(cd "$(dirname "$0")/.." && pwd)"
fail=0
sections="Activation Contract|Hard Rules|Decision Gates|Execution Steps|Output Contract|References"

for dir in "$root"/skills/*/; do
  name="$(basename "$dir")"
  file="$dir/SKILL.md"
  if [ ! -f "$file" ]; then
    echo "FALLO $name: falta SKILL.md"; fail=1; continue
  fi

  # Frontmatter
  head -1 "$file" | grep -q '^---$' || { echo "FALLO $name: sin frontmatter"; fail=1; }
  grep -q "^name: $name$" "$file" || { echo "FALLO $name: 'name' no coincide con el directorio"; fail=1; }
  grep -q '^description: "Trigger:' "$file" || { echo "FALLO $name: description debe empezar por \"Trigger:\""; fail=1; }

  # Orden de secciones
  found="$(grep -E "^## ($sections)$" "$file" | sed 's/^## //' | tr '\n' '|')"
  expected="Activation Contract|Hard Rules|Decision Gates|Execution Steps|Output Contract|References|"
  [ "$found" = "$expected" ] || { echo "FALLO $name: secciones o su orden incorrectos"; echo "  encontrado: $found"; fail=1; }

  # Presupuesto de tamaño (aprox. 4 caracteres por token, máximo 1000 tokens)
  chars="$(wc -c < "$file")"
  [ "$chars" -le 4000 ] || { echo "AVISO $name: SKILL.md tiene $chars caracteres (máx. recomendado ~4000)"; }

  # Referencias locales (directorio de la skill o raíz del proyecto)
  sfail=0
  refs="$(grep -oE '`(assets|references)/[^`]+`' "$file" | tr -d '`')"
  for ref in $refs; do
    [ -e "$dir/$ref" ] || [ -e "$root/$ref" ] || { echo "FALLO $name: referencia inexistente $ref"; sfail=1; }
  done

  if [ "$sfail" -eq 0 ]; then echo "OK    $name"; fi
  fail=$((fail + sfail))
done

exit "$fail"
