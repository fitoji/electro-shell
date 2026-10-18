---
name: pdf-leer-crear
description: "Trigger: pdf, leer pdf, extraer texto, extraer tabla, resumir pdf, crear pdf, exportar a pdf, unir pdf, temario en pdf, memoria en pdf. Lee y extrae contenido de PDF y crea PDF nuevos."
license: MIT
metadata:
  author: electro-study-shell
  version: "0.1"
---

## Activation Contract
- Activar cuando haya un PDF que leer, resumir o extraer, o cuando el entregable sea un PDF.
- No activar para editar hojas de cálculo (usar `hojas-de-calculo`) ni para redactar el contenido de la memoria (usar `memoria-tecnica-electrica`; luego exportar aquí).

## Hard Rules
- Trabajar sobre copias; no modificar el PDF original.
- Leer por partes: inventario primero, luego solo las páginas necesarias.
- Si el texto extraído está vacío, el PDF es escaneado: usar OCR o rasterizar y mirar la imagen; no inventar contenido.
- No reproducir extensamente texto con derechos de autor (libros, normas, apuntes ajenos): resumir y citar la página.
- Los valores leídos de normativa se citan con documento y página y se marcan `[VERIFICAR]` si no es la versión oficial vigente.
- Verificar el PDF creado: abrirlo, contar páginas y revisar al menos una página renderizada.

## Decision Gates
| Situación | Acción |
| --- | --- |
| Texto seleccionable | `pdfplumber`/`pypdf` (`pdftotext -layout` de poppler si está instalado) |
| Tablas | `pdfplumber` por página; comprobar columnas |
| Escaneado o sin texto | Rasterizar con `magick` (o `pdftoppm -r 150` de poppler si está) y revisar; OCR con `tesseract` si está disponible |
| PDF de más de 20 páginas | Inventario y lectura por rangos |
| Crear PDF desde Markdown o documento | Convertir a .docx/.html y exportar, o generar con `reportlab` |
| Informe con tablas y texto | `reportlab` (Platypus) |
| Unir, dividir, rotar | `pypdf` |

## Execution Steps
1. Inventario: `sh scripts/pdf-info.sh archivo.pdf` (páginas, metadatos, si tiene texto).
2. Extraer lo necesario según la tabla anterior.
3. Para crear: escribir el contenido, generar con `scripts/md-to-pdf.py` o `reportlab`, y guardar con nombre nuevo.
4. Verificar: número de páginas, texto extraíble, una página rasterizada.
5. Entregar el archivo con una línea de contexto.

## Output Contract
- Para lectura: resumen o extracto con páginas de origen.
- Para creación: ruta del PDF y número de páginas.
- Limitaciones declaradas (escaneado, tablas dudosas, OCR no disponible).
- Marcadores `[VERIFICAR]` pendientes.

## References
- `references/herramientas-pdf.md`
