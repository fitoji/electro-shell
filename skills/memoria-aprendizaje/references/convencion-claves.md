# Convención de claves y tipos

Basada en el uso recomendado por Engram: título corto y buscable, campos What / Why / Where / Learned, y un `topic_key` estable para actualizar sin duplicar.

**Pendiente de confirmar** en `DOCS.md` de Engram: parámetros exactos de `mem_save`, si admite un campo de tipo propio y su formato de `topic_key`. Hasta entonces se usa el prefijo en el título.

## topic_key
Formato: `{ámbito}/{bloque}/{tema}` en minúsculas, sin acentos, con guiones.

| Ámbito | Para qué | Ejemplos |
| --- | --- | --- |
| `electro` | Conceptos por bloque del temario | `electro/trifasica/potencia`, `electro/ca/factor-potencia` |
| `errores` | Errores propios y su corrección | `errores/caida-tension/ida-vuelta`, `errores/unidades/kw-w` |
| `normativa` | Qué ITC mirar para cada tema | `normativa/itc-bt-19/caida-tension` |
| `estilo` | Convenciones de redacción del usuario | `estilo/memoria/cabecera`, `estilo/memoria/unidades` |
| `agente` | Correcciones del usuario al agente | `agente/correccion/idioma`, `agente/correccion/formato` |
| `proyecto` | Estado de una memoria o práctica concreta | `proyecto/memoria-vivienda/estado` |

Los bloques coinciden con `skills/tutor-electrotecnia/references/temario.md`.

## Tipos (o prefijo de título)
| Tipo | Cuándo |
| --- | --- |
| `concepto` | Idea que costó entender, con su explicación que funcionó |
| `error` | Fallo del usuario en un cálculo o razonamiento, con paso y causa |
| `correccion` | El usuario corrige al agente |
| `estilo` | Preferencia de redacción o formato |
| `estado` | Punto en que quedó un proyecto, para retomarlo |

## Reglas de calidad
- Un tema, una clave: actualizar la observación existente en lugar de crear otra.
- El título debe poder encontrarse buscando la palabra que usaría el usuario (por ejemplo, "caída de tensión").
- No guardar el enunciado completo de ejercicios: guardar el patrón del error.
- Valores normativos: campo `Verificado: no` o `Verificado: sí (documento, página)`.
