#!/usr/bin/env python3
"""Uso: python3 scripts/md-to-pdf.py entrada.md salida.pdf

Convierte Markdown sencillo a PDF A4 con reportlab: títulos (#, ##, ###),
párrafos, listas (- / 1.), tablas con barras y código en bloque.
Es un conversor básico: para documentos con diseño propio usa reportlab directamente.
"""
import re
import sys
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (HRFlowable, ListFlowable, ListItem, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

FONT, FONT_BOLD = "Helvetica", "Helvetica-Bold"
for regular, bold in [
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
]:
    try:
        pdfmetrics.registerFont(TTFont("Body", regular))
        pdfmetrics.registerFont(TTFont("Body-Bold", bold))
        FONT, FONT_BOLD = "Body", "Body-Bold"
    except Exception:
        pass  # sin DejaVu: Helvetica no cubre Ω, φ, √; revisar la página renderizada

ss = getSampleStyleSheet()
body = ParagraphStyle("body", parent=ss["BodyText"], fontName=FONT, fontSize=10.5, leading=15, spaceAfter=6)
h = {n: ParagraphStyle(f"h{n}", parent=ss["Heading1"], fontName=FONT_BOLD,
                       fontSize=s, leading=s + 4, spaceBefore=12, spaceAfter=6)
     for n, s in [(1, 18), (2, 14), (3, 12)]}
code = ParagraphStyle("code", fontName="Courier", fontSize=9, leading=11, leftIndent=8, spaceAfter=6)


def inline(text):
    t = escape(text)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`(.+?)`", r'<font face="Courier">\1</font>', t)
    return t


def table(rows):
    data = [[Paragraph(inline(c.strip()), body) for c in r.strip().strip("|").split("|")] for r in rows]
    t = Table(data, repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def build(md):
    flow, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            i += 1; block = []
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i]); i += 1
            flow.append(Preformatted("\n".join(block), code))
        elif re.match(r"^\s*(-{3,}|\*{3,})\s*$", line):
            flow.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceBefore=6, spaceAfter=6))
        elif m := re.match(r"^(#{1,3})\s+(.*)", line):
            flow.append(Paragraph(inline(m.group(2)), h[len(m.group(1))]))
        elif line.strip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                if not re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i]):
                    rows.append(lines[i])
                i += 1
            flow.append(table(rows)); flow.append(Spacer(1, 6)); continue
        elif re.match(r"^\s*([-*]|\d+\.)\s+", line):
            ordered = bool(re.match(r"^\s*\d+\.", line)); items = []
            while i < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                items.append(ListItem(Paragraph(inline(re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i])), body)))
                i += 1
            flow.append(ListFlowable(items, bulletType="1" if ordered else "bullet", leftIndent=24)); continue
        elif line.strip():
            para = [line]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"^(#|\||```|\s*([-*]|\d+\.)\s)", lines[i + 1]):
                i += 1; para.append(lines[i])
            # Dos espacios al final de línea = salto de línea duro (como en Markdown)
            html = "".join(inline(l.strip()) + ("<br/>" if l.endswith("  ") else " ") for l in para)
            flow.append(Paragraph(html.rstrip(), body))
        i += 1
    return flow


def footer(canvas, doc):
    canvas.setFont(FONT, 8)
    canvas.drawRightString(A4[0] - 2.5 * cm, 1.5 * cm, f"Página {doc.page}")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        md = f.read()
    doc = SimpleDocTemplate(sys.argv[2], pagesize=A4, leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                            topMargin=2.5 * cm, bottomMargin=2.5 * cm)
    doc.build(build(md), onFirstPage=footer, onLaterPages=footer)
    print(f"PDF creado: {sys.argv[2]}")


if __name__ == "__main__":
    main()
