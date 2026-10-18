# Modelos de hoja para electrotecnia

Disposición orientativa. Las fórmulas son las de `skills/revisor-calculos-electricos/references/formulas.md`. Los valores normativos van en celdas aparte marcadas `[VERIFICAR]`.

## 1. Cuadro de cargas y secciones
Hoja `Parámetros` (datos de entrada):

| Celda | Concepto | Valor |
| --- | --- | --- |
| B2 | Tensión monofásica (V) | 230 |
| B3 | Tensión trifásica de línea (V) | 400 |
| B4 | Conductividad γ (m/(Ω·mm²)) | [VERIFICAR: ITC-BT-19 / temperatura] |
| B5 | Caída máxima admisible (%) | [VERIFICAR: ITC-BT-19] |

Hoja `Circuitos`:

| Col | Contenido | Tipo |
| --- | --- | --- |
| A | Circuito | dato |
| B | Potencia P (W) | dato |
| C | cos φ | dato |
| D | Longitud L (m) | dato |
| E | Sección S (mm²) | dato |
| F | Intensidad I (A) | `=B2/(Parámetros!$B$2*C2)` |
| G | Caída e (V) | `=2*D2*F2*C2/(Parámetros!$B$4*E2)` |
| H | Caída e (%) | `=100*G2/Parámetros!$B$2` |
| I | ¿Cumple? | `=IF(H2<=Parámetros!$B$5,"Sí","No")` |

Para trifásica sustituir F y G por las fórmulas con √3: `=B2/(SQRT(3)*Parámetros!$B$3*C2)` y `=SQRT(3)*D2*F2*C2/(Parámetros!$B$4*E2)`.

## 2. Presupuesto
Columnas: concepto, unidad, cantidad, precio unitario (€), importe `=C2*D2`; fila de total `=SUM(E2:E20)`; IVA en celda de parámetros.

## 3. Registro de prácticas o notas
Columnas: fecha, tema, ejercicios hechos, aciertos, observaciones; resumen con `=COUNTIF` y `=AVERAGE`.

## Formato
- Cabecera en negrita con relleno suave; filas de datos sin fondo.
- Entradas en azul, fórmulas en negro.
- Números con formato explícito (`0.00` para amperios y voltios, `0.0%` para porcentajes).
- Anchos de columna ajustados y primera fila inmovilizada.
