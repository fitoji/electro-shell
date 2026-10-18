# ITC-BT-19, Tabla 1 — intensidades admisibles (A) al aire 40 ºC

Transcripción manual de una tabla que el BOE **no publica como tabla HTML**: en
`cache/bloque_ib-19.xml` aparece solo como `<img src=".../18099_image32.png" width="1504" height="1741">`.
No existe, por tanto, extracción automática posible: estas cifras salen de leer el escaneo.

## Procedencia

| Campo | Valor |
| --- | --- |
| Norma | BOE-A-2002-18099 (REBT) |
| Grupo | ITC-BT-19, apartado 2.2.3 «Intensidades máximas admisibles» |
| Fuente primaria | `md/ITC-BT-19.md` líneas 77-83 |
| Imagen | `imgs/18099_image32.png` (1504 × 1741 px) |
| Fecha de transcripción | 2026-10-18 (primer pase visual); 2026-10-18 segundo pase OCR |
| Ficheros | `ITC-BT-19_tabla1-intensidades-aire-40C.csv`, `ITC-BT-19_tabla1-cabecera.csv` |

## Método

1. Detección de los muros de la rejilla por análisis de píxeles (líneas verticales
   en `x = 618, 698, 777, 858, 937, 1016, 1096, 1177, 1257, 1338, 1418, 1499`;
   horizontales en `y = 3, 119, 234, 350, 466, 582, 698, 814, 930, 971, 1341`),
   para situar cada etiqueta de cabecera en su columna real y no a ojo.
2. Lectura de la matriz numérica en dos mitades ampliadas al 330 % con solape en la
   columna 6, de modo que la misma columna se lee dos veces (16/22/30/37/52/70/88/110/133/171/207/240/278/317/374/423 A coinciden en ambas lecturas).
3. Comprobación automática de monotonía: en cada columna la intensidad crece
   estrictamente con la sección. Ninguna serie la incumple.

## Segundo pase independiente (OCR, 2026-10-18)

Lectura mecánica con `tesseract` 5.5.3, ciega al método del primer pase:

- **Pasada de banda completa**: recorte de la matriz (`-crop 1504x412+0+930`, ×3,
  `--psm 6`, salida TSV); reconstrucción de celdas por rejilla (muros medidos en
  `x`, líneas de `tesseract` en `y`) y comparación celda a celda contra el CSV.
  Resultado: 100/176 celdas idénticas al CSV, 50 sin lectura (los guiones «-»
  no emiten token: coherente con las 33 celdas a guion y las columnas vacías),
  26 discrepancias.
- **Adjudicación celda a celda**: recortes por celda a ×10/×12 con variantes de
  umbral y morfología, `--psm 7/8/13`, lista blanca de dígitos.
- **Pruebas estructurales independientes del OCR**: monotonía estricta por
  columna, razón entre columnas adyacentes (familia c2/c3 = 0.88–0.93 y
  c2/c4 decreciente 0.85→0.80; ambas sitúan c2 de 35 mm² en ≈77–78, no 73) e
  incrementos constantes entre filas finales (c7 +65/+65, c8 +69/+69,
  c11 +110/+110), que confirman 484/386/711/821 frente a las lecturas de OCR
  494/326/«7»/921.

**Corrección aplicada al CSV**: (240 mm², c5) **330 → 350 A**. Nueve lecturas OCR
independientes terminan en «50» (350/1450/4350/950) y las pruebas estructurales
coinciden: el incremento de c5 en las últimas filas pasa de +33/+74 (con 330,
  rotura del patrón) a +53/+54 (con 350, constante como en c7/c8/c11), y la razón
c5/c4 = 350/315 = 1.111 encaja con la familia de las filas vecinas (1.102/1.108)
mientras que 330/315 = 1.048 no. La matriz corregida re-verifica rectangularidad
(16 × 12 campos) y monotonía estricta.

**Sesgo de OCR documentado**: el dígito «8» impreso se lee como 9 o 2 con
  regularidad (821→921, 484→494, 284→294, 386→326, 284→«194»). Las celdas donde
  solo el primer pase visual y la estructura sostienen el valor quedan así:
  77 (c2, 35 mm²), 284 (c8, 120 mm²), 386 (c8, 185 mm²), 711 (c11, 240 mm²,
  la banda completa leyó «7It»), 484 y 821 (300 mm²).

## Convenciones

- `-` reproduce el guion impreso: el escaneo no da valor para esa combinación.
- El escaneo imprime coma decimal; aquí se normaliza a punto (`11,5` → `11.5`) sin
  alterar ningún dígito.
- Cabecera: `3x` / `2x` son conductores cargados, y `XLPE o EPR` el aislamiento.
  Se recoge **la cabecera tal como está impresa**, en una rejilla de 8 métodos
  (A, A2, B, B2, C, E, F, G) × 11 columnas.

## Limitación declarada — `[VERIFICAR]`

La banda de cabecera del escaneo **se solapa a sí misma**: la pareja de PVC del
método A cae en las columnas 2-3, mientras que la de A2 cae en 1-2, de modo que una
misma columna recoge etiquetas de métodos distintos (p. ej. c4 acumula
«A2 3x XLPE o EPR», «B 3x PVC» y «B2 2x PVC»), y B2 imprime sus dos etiquetas XLPE
en las columnas 6 y 8, dejando la 7 vacía.

Eso no es un error de transcripción: es cómo está impreso el escaneo del BOE, y no
se puede resolver desde el ráster. Los **valores numéricos son fiables**; la
correspondencia exacta columna → (método, tipo de cable, conductores, aislamiento)
debe confirmarse contra la norma que el propio apartado 2.2.3 declara aplicable:

> Las intensidades máximas admisibles, se regirán en su totalidad por lo indicado en
> la Norma UNE 20.460-5-523 y su anexo Nacional.

`[VERIFICAR: UNE 20.460-5-523, correspondencia cabecera-columna de la tabla de intensidades admisibles]`

Hasta que esa correspondencia se confirme, **no se debe elegir columna por posición
para justificar una protección**. Sí se puede usar la tabla para localizar el valor
de una combinación ya identificada en la norma.

## Pie de tabla transcrito

1. A partir de 25 mm² de sección.
2. Incluyendo canales para instalaciones -canaletas- y conductos de sección no circular.
3. O en bandeja no perforada.
4. O en bandeja perforada.
5. D es el diámetro del cable.
