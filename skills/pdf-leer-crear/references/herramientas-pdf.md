# Herramientas PDF

## Leer
```bash
# Inventario
pdfinfo archivo.pdf
pdftotext -layout -f 1 -l 5 archivo.pdf -        # páginas 1 a 5, conserva columnas
pdftoppm -r 150 -f 3 -l 3 -png archivo.pdf p     # página 3 como imagen
```

```python
import pdfplumber
with pdfplumber.open("archivo.pdf") as pdf:
    page = pdf.pages[2]
    texto = page.extract_text()
    tablas = page.extract_tables()
```

## Detectar escaneado
Si `pdftotext` devuelve texto vacío o casi vacío en varias páginas, el PDF es una imagen. Rasterizar y leer la imagen; si hay `tesseract` instalado, usarlo para OCR y declarar que el texto es reconocimiento óptico.

## Unir, dividir, rotar
```python
from pypdf import PdfReader, PdfWriter
w = PdfWriter()
for f in ["a.pdf", "b.pdf"]:
    for p in PdfReader(f).pages:
        w.add_page(p)
with open("unido.pdf", "wb") as out:
    w.write(out)
```

## Crear
- Desde Markdown simple: `python3 scripts/md-to-pdf.py entrada.md salida.pdf` (títulos, párrafos, listas y tablas básicas).
- Desde un documento: exportar a .docx y convertir con `soffice --headless --convert-to pdf`.
- Informes con diseño propio: `reportlab` (Platypus: `Paragraph`, `Table`, `Spacer`, `PageBreak`).

## Convenciones para documentos técnicos
- Tamaño A4, márgenes de 2,5 cm, interlineado 1,15.
- Numeración de página en el pie y título del documento en la cabecera.
- Tablas con título y cabecera diferenciada; unidades en la cabecera.
- Letra con ñ, acentos y símbolos (Ω, φ, √, ²): usar una fuente que los incluya y comprobarlo en la página renderizada.

## Verificación
```bash
pdfinfo salida.pdf | grep Pages
pdftotext salida.pdf - | head
pdftoppm -r 100 -f 1 -l 1 -png salida.pdf check
```
