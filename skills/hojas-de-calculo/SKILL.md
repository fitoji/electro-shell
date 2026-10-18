---
name: hojas-de-calculo
description: "Trigger: hoja de cálculo, planilla, excel, xlsx, csv, tabla con fórmulas, cuadro de cargas, presupuesto, editar planilla. Crea y edita hojas de cálculo con fórmulas vivas y las comprueba."
license: MIT
metadata:
  author: electro-study-shell
  version: "0.1"
---

## Activation Contract
- Activar cuando el archivo principal sea una hoja de cálculo (.xlsx, .xlsm, .csv, .tsv): crearla, editarla o limpiarla.
- No activar si el entregable es un PDF o un documento de texto (usar `pdf-leer-crear` o `memoria-tecnica-electrica`).

## Hard Rules
- Trabajar sobre una copia: nunca modificar el original subido.
- Usar fórmulas de Excel (`=B2*C2`) en las celdas calculadas, no valores calculados en Python.
- Datos de entrada en celdas propias; no escribir constantes dentro de las fórmulas.
- Unidades en la cabecera de cada columna.
- Tras guardar, recalcular y comprobar que no hay errores (`#REF!`, `#DIV/0!`, `#NAME?`, `#VALUE!`).
- Valores normativos (conductividad, caídas máximas, factores): si el corpus del proyecto está (`references/rebt_salida/tablas/_v2/`), tomar el valor de ahí y anotar la procedencia; si no, celda marcada `[VERIFICAR: ITC-BT-XX]`.

## Decision Gates
| Situación | Acción |
| --- | --- |
| Hay que editar un .xlsx existente | Cargar con `openpyxl`, conservar formato y fórmulas, guardar copia |
| Solo se necesita analizar datos | Leer con `openpyxl`/`pdfplumber` según el origen (pandas no instalado); no generar fichero si no se pide |
| Fórmulas en el archivo y se necesitan sus valores | Recalcular con `scripts/recalc-xlsx.sh` y leer con `data_only=True` |
| Plantilla eléctrica (cargas, secciones) | Partir de `references/modelos-electricos.md` |
| Cálculo crítico | Pasarlo por `revisor-calculos-electricos` |

## Execution Steps
1. Definir columnas, unidades y qué es dato y qué es fórmula.
2. Crear o cargar con `openpyxl`; escribir fórmulas, formato de número y anchos de columna.
3. Guardar en una copia con nombre nuevo.
4. Ejecutar `sh scripts/recalc-xlsx.sh archivo.xlsx` y revisar errores.
5. Entregar el archivo con una línea de contexto.

## Output Contract
- Ruta del archivo creado o modificado.
- Resultado del recálculo: sin errores o lista de celdas con error.
- Supuestos y marcadores `[VERIFICAR]` pendientes.

## References
- `references/modelos-electricos.md`
