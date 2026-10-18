---
name: memoria-aprendizaje
description: "Trigger: me equivoqué, corrección, error frecuente, apunta esto, recuerda, qué he aprendido, repaso de errores, inicio de sesión, fin de sesión, memoria persistente, Engram. Guarda y recupera aprendizajes, errores y correcciones en Engram."
license: MIT
metadata:
  author: electro-study-shell
  version: "0.1"
---

## Activation Contract
- Activar al empezar y cerrar sesión, cuando el usuario corrige al agente, cuando el revisor detecta un error y cuando se resuelve un ejercicio o concepto costoso.
- Otras skills la invocan en sus pasos de memoria. No activar para guardar salida cruda ni conversación completa.

## Hard Rules
- Guardar solo conocimiento duradero: concepto que costó, error con su corrección, corrección del usuario al agente, decisión de estilo.
- Buscar antes de guardar (`mem_search`); si el tema existe, actualizar (`mem_update`) con su `topic_key`, no duplicar.
- Un valor normativo se guarda como `no verificado` salvo que cite documento y página oficiales. Recuperarlo de memoria no lo verifica: volver a comprobarlo.
- Si el usuario contradice la memoria, prevalece el usuario: actualizar la observación.
- No guardar datos personales ni de terceros más allá de lo necesario para aprender, ni secretos.
- Si la memoria no está disponible, continuar sin ella y decirlo.

## Decision Gates
| Situación | Acción |
| --- | --- |
| El usuario corrige al agente | Guardar al instante como `correccion` |
| El revisor encuentra un error de cálculo | Guardar como `error` con paso y causa |
| Mismo error por segunda vez | Actualizar la observación y marcar `recurrente` |
| Ejercicio resuelto sin fallos | No guardar, salvo que cierre un tema |
| Observación obsoleta o contradictoria | `mem_review`; actualizar o descartar |
| Clasificar la observación | `type` libre (confirmado contra el Engram vivo): `error`, `concepto`, `correccion`, `estilo`, `decision`; con `topic_key` para el upsert |

## Execution Steps
1. Inicio: `mem_current_project`, `mem_context` y `mem_search` del tema; usarlo para adaptar la sesión.
2. Durante: al cumplirse un disparador, componer la observación con `assets/plantillas-observacion.md` y la clave de `references/convencion-claves.md`.
3. Guardar o actualizar; no narrar el guardado salvo error.
4. Cierre: `mem_session_summary` con lo aprendido, errores y pendientes; luego `mem_session_end`.

## Output Contract
- Observaciones creadas o actualizadas, con su `topic_key`.
- Errores recurrentes detectados.
- Valores marcados `no verificado`.
- Aviso si la memoria no estaba disponible.

## References
- `references/convencion-claves.md`
- `assets/plantillas-observacion.md`
