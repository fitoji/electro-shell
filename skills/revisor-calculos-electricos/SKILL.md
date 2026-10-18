---
name: revisor-calculos-electricos
description: "Trigger: revisa los cálculos, comprueba sección, caída de tensión, intensidad, protecciones, verificar cálculo eléctrico. Revisión independiente de cálculos eléctricos de baja tensión."
license: MIT
metadata:
  author: electro-study-shell
  version: "0.1"
---

## Activation Contract
- Activar para comprobar cálculos de intensidad, sección, caída de tensión, potencia y protecciones.
- Actuar como verificador independiente: recalcular desde los datos, no desde el resultado dado.
- No activar para redactar documentos ni para enseñar teoría.

## Hard Rules
- Recalcular con fórmula, datos con unidades, sustitución y resultado; no aceptar el resultado aportado.
- Ejecutar la aritmética en código (`python -c` o similar), no de cabeza.
- Declarar los datos que faltan en lugar de suponerlos.
- Los límites normativos (caída máxima, secciones mínimas, intensidades admisibles) se toman del corpus del proyecto (`references/rebt_salida/`), si existe, citando `[FUENTE: …]`; lo que no esté en el corpus se marca `[VERIFICAR: ITC-BT-XX]`, no se da de memoria.
- Redondeo comercial a 2 decimales: comparar tras redondear ambos valores; una diferencia que desaparece al redondear es coincidencia, no se absorbe con tolerancias.
- Un cálculo es "correcto" solo si coinciden fórmula, unidades y resultado.

## Decision Gates
| Situación | Acción |
| --- | --- |
| Falta un dato (longitud, cos φ, tipo de instalación) | Listar el dato y no concluir |
| Difieren solo en redondeo (2 decimales) | Marcar coincidente |
| Diferencia que no desaparece al redondear | Mostrar ambos cálculos y localizar el paso del error |
| Unidades mezcladas | Convertir y señalar |
| Cumple el cálculo pero el criterio normativo no está verificado | Marcar "cumple condicionado a verificación" |

## Execution Steps
1. Extraer datos y fórmulas del texto revisado.
2. Recalcular cada línea con código.
3. Comparar con los valores del texto y clasificar cada uno.
4. Revisar coherencia entre apartados (potencia, intensidad, sección, protección).
5. Emitir informe.
6. Guardar con `memoria-aprendizaje` cada error confirmado (paso y causa) y marcar `recurrente` si ya estaba registrado. El revisor no consulta la memoria para decidir si un cálculo es correcto: recalcula siempre.

## Output Contract
- Tabla: cálculo, valor del texto, valor recalculado, estado.
- Errores localizados con el paso y la corrección propuesta.
- Datos faltantes y criterios normativos pendientes de verificar.
- Riesgos residuales.

## References
- `references/formulas.md`
- Corpus normativo del proyecto: `references/rebt_salida/md/` (texto) y `references/rebt_salida/tablas/_v2/` (valores, con `_manifest.json` de procedencia)
