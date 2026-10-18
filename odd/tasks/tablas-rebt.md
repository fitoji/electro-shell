# tablas-rebt — recuperar tablas normativas rotas del corpus REBT

Corpus `references/rebt_salida/`: 73 tablas HTML en la versión vigente de `cache/*.xml` y 73 CSV en `tablas/`. El defecto real no era falta de tablas sino celdas aplastadas por el extractor anterior. Una única tabla crítica existe solo como escaneo.

## Specs

**S1** — Pedido original, verbatim:
> aqui https://www.boe.es/biblioteca_juridica/codigos/codigo.php?modo=2&id=326_Reglamento_electrotecnico_para_baja_tension_e_ITC tiene una api y puedes buscar las tablas que estan rotas

**S2** — Alcance autorizado por el usuario: `Todo: XML primero, luego las de imagen`.

**S3** — Todas las tablas HTML de la versión vigente de cada bloque se re-extraen desde `cache/*.xml` con un parser que respete `rowspan`, `colspan`, las subfilas (`<td>` con varios `<p>`) y `<tfoot>`.

**S4** — La extracción no pierde contenido: toda celda `td`/`th` del XML queda representada en el CSV. Verificación contra la fuente, no contra la extracción anterior.

**S5** — La tabla que el BOE publica solo como escaneo (`<img>` sin `<table>`) se transcribe desde el PNG local con doble pasada de verificación independiente: ITC-BT-19 Tabla 1 (intensidades admisibles al aire 40 ºC, `18099_image32.png`). Las tablas de ITC-BT-07 con pictogramas en la cabecera no requieren transcripción: sus cifras están en el XML y solo la cabecera es imagen.

**S6** — No se sobrescribe `tablas/`: la extracción va a `tablas/_v2/` y la transcripción manual a `tablas/_verificadas/`. Los 73 CSV actuales quedan intactos como referencia.

**S7** — Las imágenes referenciadas en `md/*.md` existen todas en `imgs/`; los md deben apuntar a la ruta local, no a la URL de boe.es.

**S8** — Cada tabla extraída o transcrita declara su procedencia: bloque y tabla de origen del XML, o nombre del PNG y fecha de transcripción.

## Tasks

| ID | Specs | Ruta | Estado |
| --- | --- | --- | --- |
| T1 | — | documento de tarea | hecho |
| T2 | S3, S6, S8 | `scripts/extraer-tablas-rebt.py` | hecho |
| T3 | S3, S4 | ejecución + verificación contra el XML | hecho |
| T4 | S5, S8 | transcripción ITC-BT-19 Tabla 1 | hecho |
| T5 | S5 | segundo pase independiente | hecho (2026-10-18, OCR; ver L7) |
| T6 | S7 | rutas de imagen locales en md | hecho |
| T7 | S8 | cobertura y pendientes en README | hecho |

## Log

**L1** — Pedido original, verbatim:
> aqui https://www.boe.es/biblioteca_juridica/codigos/codigo.php?modo=2&id=326_Reglamento_electrotecnico_para_baja_tension_e_ITC tiene una api y puedes buscar las tablas que estan rotas

**L2** — Diagnóstico previo a la implementación (evidencia):
- `cache/*.xml` son respuestas de la API de datos abiertos del BOE, con las tablas en HTML intacto.
- Las 73 extraídas fallan porque cada `<td>` puede contener varios `<p>` (subfilas) y porque hay `colspan`/`rowspan`; el extractor anterior los aplastó. Evidencia: `tablas/ITC-BT-19_t01.csv` colapsa `S ≤ 16`, `16< S ≤ 35`, `S > 35` en una sola celda.
- ITC-BT-19 Tabla 1 no existe como `<table>`: el XML la publica como `<img src=".../18099_image32.png" width="1504" height="1741">`.
- Las imágenes referenciadas en los md están todas presentes en `imgs/`; el fallo es de rutas, no de descarga.

**L3** — Decisión del usuario sobre alcance: `todo` (XML primero, luego las tablas solo-imagen).

**L4** — Correcciones al diagnóstico de L2 tras medir con datos, no con impresiones:
- «93 `<table>` frente a 73 CSV» era un artefacto de contar todas las versiones históricas de cada bloque. En la versión vigente hay exactamente 73, que son las 73 extraídas: **no había 20 tablas sin extraer**. S4 original queda obsoleta.
- «38 CSV con columnas irregulares» era un artefacto de contar comas por línea. Parseados con `csv`, los 73 CSV anteriores son rectangulares: **0 filas irregulares**. El defecto real es el colapso de subceldas en 27 tablas, no la irregularidad.
- El extractor anterior descartaba `<tfoot>`: ITC-BT-02_t01 perdía 21 notas al pie. Detectado por la verificación contra el XML, corregido.
- Solo hay **1** tabla realmente solo-imagen en todo el corpus, no ~6: ITC-BT-19 Tabla 1. El alcance de S5 se reduce a esa tabla.
- Resultado de T3: 73/73 tablas, 0 filas irregulares, **0 celdas del XML ausentes del CSV**, 27 tablas con subfilas expandidas, 4 con celdas-imagen.

**L5** — Estado de T4/T5/T6 (evidencia):
- T4 cerrado: `tablas/_verificadas/ITC-BT-19_tabla1-intensidades-aire-40C.csv` (16 filas × 11 columnas, guiones reproducidos, coma decimal normalizada a punto sin alterar dígitos), `..._cabecera.csv` (8 métodos × 11 columnas) y `..._PROCEDENCIA.md` (fuente, fecha 2026-10-18, método, limitaciones).
- Comprobaciones automáticas: anchura rectangular exacta (12 y 13 campos), monotonía estricta por columna (16/16 series OK, ninguna intensidad decrece al crecer la sección), doble lectura de la matriz por mitades con solape en la columna 6 (ambas lecturas coinciden), relectura de las filas críticas 25 y 300 mm² por recortes independientes al 500 %.
- T5 bloqueado parcialmente: el gate de verificación no admite subagente para este cambio y no hay OCR (`tesseract` no instalado). El segundo pase hecho inline no es ciego (mismo lector). La correspondencia cabecera-columna del escaneo —que se solapa a sí misma— queda declarada como `[VERIFICAR: UNE 20.460-5-523]` en el PROCEDENCIA.md, conforme a la regla dura de no inventar valores normativos.
- T6 en curso, delegado a worker (superficie: `references/rebt_salida/md/*.md`): 73 URLs `boe.es/datos/imagenes` en 12 md, 47 basenames distintos, los 47 presentes en `imgs/`; 16 PNG sin referenciar de otras normas no se tocan.

**L6** — Cierre de T6/T7 (evidencia):
- T6 hecho y verificado inline tras el worker: 73/73 sustituciones `![imagen](https://www.boe.es/datos/imagenes/disp/…)` → `![imagen](../imgs/…)`; 0 URLs remotas restantes en `md/`; los 63 basenames referenciados existen en `imgs/` (0 faltantes); 54 md intactos; 12 archivos tocados (ITC-BT-07 con 17, ITC-BT-24/27/52 con 10 cada uno…).
- Corrección de diagnóstico: el conteo previo de «47 basenames referenciados, 16 PNG sin referencia» era un artefacto de patrón (`[0-9]+_image[0-9]+\.png` no casa con nombres tipo `05089_8907.png` ni `13681_4524.png`, de otras normas del BOE). Real: **63 basenames distintos, los 63 PNG del corpus referenciados**. Los demás "images" embebidos en los md son fórmulas MathML en base64, no imágenes remotas.
- T7 hecho: `README.md` gana la sección «Corpus normativo (`references/rebt_salida/`)» con la tabla de capas y estados, los comandos reproducibles del extractor (`extraer`, `--verify`), la regla de uso de la capa numérica y, en «Pendiente de confirmar», los pendientes reales del corpus.

**L7** — Cierre de T5 (2026-10-18, el usuario instaló `tesseract`; evidencia):
- Segundo pase mecánico y ciego al método del primero: `tesseract` 5.5.3 sobre el recorte de la matriz (`-crop 1504x412+0+930`, ×3, `--psm 6`, TSV), reconstrucción por rejilla con las líneas del propio tesseract y los muros medidos en x. Resultado: 100/176 celdas idénticas, 50 sin lectura (coherente con los guiones), 26 discrepancias adjudicadas celda a celda (×10/×12, umbrales, morfología, `--psm 7/8/13`, lista blanca de dígitos) más pruebas estructurales (monotonía, razones entre columnas adyacentes, incrementos constantes en filas finales).
- **Corrección real encontrada por el segundo pase**: (240 mm², c5) **330 → 350 A** corregido en el CSV; 9 lecturas OCR terminan en «50» y las pruebas estructurales (+53/+54 constantes como c7/c8/c11; razón c5/c4 = 1.111 en la familia de filas vecinas frente a 1.048) confirman 350. La matriz corregida re-verifica rectangularidad 16×12 y monotonía estricta.
- Sesgo de OCR documentado: el «8» impreso se lee como 9 o 2 (821→921, 484→494, 284→294, 386→326); las celdas sostenidas solo por primer pase + estructura quedan listadas en el PROCEDENCIA.md.
- Error propio de proceso corregido a mitad de pase: el primer lote de recortes por celda usó un índice de fila desplazado (5 celdas leídas de la fila superior); detectado porque las lecturas «338/601/4x9» casaban con la fila anterior, repetido con índices correctos.
- Queda abierto (externo): la correspondencia cabecera-columna `[VERIFICAR: UNE 20.460-5-523]`, no resoluble desde el ráster.
