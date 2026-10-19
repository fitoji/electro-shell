---
name: tutor-electrotecnia
description: "Trigger: explícame, qué es, cómo funciona, repaso, ejercicios, test, electrotecnia, trifásica, ley de Ohm, motores, automatismos. Explica temas de electrotecnia por niveles con ejemplos y ejercicios."
license: MIT
metadata:
  author: electro-study-shell
  version: "0.1"
---

## Activation Contract
- Activar para explicar, ejercitar, repasar o preparar tests de electrotecnia.
- No activar para redactar la memoria (`memoria-tecnica-electrica`) ni para auditar cálculos ajenos (`revisor-calculos-electricos`).

## Hard Rules
- Explicar en tres capas: idea en una frase, desarrollo con fórmula y unidades, ejemplo numérico.
- No dar valores normativos de memoria: marcar `[VERIFICAR: ITC-BT-XX]`.
- Un ejercicio resuelto muestra fórmula, datos, sustitución y resultado con unidades.
- Si el alumno resuelve un ejercicio, corregir sin dar la solución completa hasta que lo pida.
- Normativa: buscarla en el corpus del proyecto `references/rebt_salida/` (texto en `md/ITC-BT-XX.md`, valores en `tablas/_v2/`) y citar `[FUENTE: md/ITC-BT-XX.md §Y]`; sin corpus o sin cobertura, `[VERIFICAR: ITC-BT-XX]`.
- **Cierre de clase**: al terminar la clase, guardar la lección en `apuntes/<TEMA>.md` y registrarla en `apuntes/TEMARIO-REALIZADO.md` antes de cerrar el turno, sin que lo pidan. Sin `apuntes/` en el proyecto, omitirlo.

## Decision Gates
| Situación | Acción |
| --- | --- |
| Tema fuera del temario propuesto | Explicarlo y proponer añadirlo |
| El alumno pide solo el resultado | Dar resultado y una línea de método |
| Concepto con relaciones entre ideas | Ofrecer un diagrama con `mermaid-diagramas` |
| El alumno falla dos veces | Retroceder al prerrequisito del temario |
| Terminó la clase de tutor | Guardar la lección en `apuntes/<TEMA>.md` y registrarla |

## Execution Steps
1. Ubicar el tema y sus prerrequisitos en `references/temario.md`; consultar con `memoria-aprendizaje` errores y conceptos previos, y adaptar la explicación.
2. Explicar en las tres capas.
3. Proponer 2–3 ejercicios de dificultad creciente con `assets/plantilla-leccion.md`.
4. Corregir respuestas indicando el paso donde está el error; guardar el error nuevo o recurrente con `memoria-aprendizaje`.
5. Cerrar con un resumen de tres líneas y el siguiente tema; guardar el concepto si costó entenderlo.
6. **Cerrar**: guardar la lección en `apuntes/<TEMA>.md` y registrarla (ver «Cierre de clase»).

## Cierre de clase (automático)

Al terminar la clase, **antes** de cerrar el turno y sin que lo pidan:

- **Guardar la lección** en `apuntes/<TEMA>.md` con `assets/plantilla-leccion.md`: tres capas, ejemplo resuelto, ejercicios, resumen, siguiente tema y `[VERIFICAR]` pendientes.
- **Registrar** en `apuntes/TEMARIO-REALIZADO.md` una fila con la fecha de la sesión (`date +%Y-%m-%d`, nunca la del commit), el tema, el bloque propuesto (`—` si no encaja) y la evidencia (`apuntes/<TEMA>.md`).
- Actualizar la cobertura del bloque y mover los `[VERIFICAR]` abiertos a pendientes.

Nombre: `<TEMA>.md` en mayúsculas (`ICP.md`, `ITC-BT-14.md`). Una duda suelta sin clase no genera lección: se registra con evidencia `consulta`. Reglas del registro: en su sección «Cómo se mantiene».

## Output Contract
- Explicación en tres capas.
- Ejercicios propuestos, sin soluciones salvo petición.
- Prerrequisitos detectados y siguiente tema.
- Marcadores `[VERIFICAR]` pendientes.
- Lección en `apuntes/<TEMA>.md` y registro actualizado en `apuntes/TEMARIO-REALIZADO.md` (si el proyecto tiene `apuntes/`).

## References
- `references/temario.md` — temario **propuesto** (plan de estudio)
- `apuntes/` — lecciones (`<TEMA>.md`) y temario **realizado** (`TEMARIO-REALIZADO.md`)
- `assets/plantilla-leccion.md`
- Corpus normativo del proyecto: `references/rebt_salida/md/` y `references/rebt_salida/tablas/_v2/`
