# Sintaxis y límites de Mermaid

## Errores frecuentes
- Paréntesis, acentos o dos puntos en etiquetas sin comillas: usar `A["Texto (con paréntesis)"]`.
- La palabra `end` en minúsculas como nodo rompe flowcharts: usar `End` o `"end"`.
- Flechas mal formadas: usar `-->`, `-.->`, `==>`.
- Etiquetas en flechas: `A -->|"texto"| B`.
- En `stateDiagram-v2` las transiciones se etiquetan con `: texto`.

## Qué no puede hacer
- No dibuja simbología eléctrica normalizada (contactos, bobinas, magnetotérmicos).
- No es un editor de planos ni de esquemas multifilares.
- Para esquemas normalizados considerar herramientas específicas de CAD eléctrico y citarlas como alternativa; no simularlas con Mermaid.

## GRAFCET aproximado
Se puede aproximar la secuencia con `stateDiagram-v2` (etapas = estados, transiciones = condiciones). Avisar siempre de que no es notación GRAFCET normalizada.

## Validación
`scripts/validate-mermaid.sh` usa `mmdc` (paquete `@mermaid-js/mermaid-cli`) si está instalado. Si no lo está, indicar "no validado".
