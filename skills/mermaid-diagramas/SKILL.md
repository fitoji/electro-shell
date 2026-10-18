---
name: mermaid-diagramas
description: "Trigger: diagrama, mermaid, flujo, diagrama de bloques, secuencia, estados, GRAFCET aproximado, esquema. Genera diagramas Mermaid válidos y los valida con mmdc."
license: MIT
metadata:
  author: electro-study-shell
  version: "0.1"
---

## Activation Contract
- Activar cuando se pida un diagrama, flujo, mapa conceptual o secuencia.
- No activar para esquemas eléctricos normalizados (unifilar, multifilar): Mermaid no los representa.

## Hard Rules
- Entregar en bloque ```mermaid, una sola idea por diagrama.
- Etiquetas con texto entre comillas si llevan paréntesis, acentos o símbolos.
- Sin colores ni estilos salvo que se pidan.
- Máximo ~15 nodos por diagrama; si excede, dividir.
- Avisar de la limitación cuando el tema pida simbología eléctrica normalizada.

## Decision Gates
| Contenido | Tipo Mermaid |
| --- | --- |
| Proceso o procedimiento | `flowchart TD` |
| Arquitectura o bloques de una instalación | `flowchart LR` |
| Secuencia de automatismo (marcha/paro) | `stateDiagram-v2` |
| Interacción entre elementos en el tiempo | `sequenceDiagram` |
| Temario o ideas relacionadas | `mindmap` |
| Esquema unifilar normalizado | No usar Mermaid; ofrecer bloques y avisar |

## Execution Steps
1. Identificar el tipo según la tabla.
2. Escribir el diagrama partiendo de `assets/ejemplos.md`.
3. Si `mmdc` está disponible, validar: `sh scripts/validate-mermaid.sh archivo.mmd`.
4. Corregir errores de sintaxis y reentregar.
5. Añadir una frase de lectura del diagrama.

## Output Contract
- Bloque ```mermaid listo para pegar.
- Estado de validación: validado con `mmdc` o no validado.
- Limitaciones declaradas.

## References
- `assets/ejemplos.md`
- `references/sintaxis-y-limites.md`
