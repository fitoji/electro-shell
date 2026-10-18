# electro-study-shell

Paquete de **skills** y **prompts** para [Pi](https://pi.dev) que convierte un agente en tutor y redactor técnico de electrotecnia: explica temas por niveles, redacta memorias técnicas de BT, verifica cálculos y genera diagramas Mermaid — todo anclado al corpus normativo del REBT, con citas `[FUENTE]` para lo verificado y `[VERIFICAR]` para lo pendiente.

Pensado para un alumno de ciclo formativo de grado superior (Sistemas Electrotécnicos y Automatizados). No sustituye al técnico competente ni al proyecto visado.

## Inicio rápido

1. Valida el paquete: `sh scripts/validate-skills.sh` → esperado: 7 líneas `OK` y exit 0.
2. Instálalo como paquete Pi (documento: docs de Pi, «Pi Packages»):
   ```sh
   pi install "/ruta/absoluta/a/electro-study-shell"      # personal (~/.pi/agent/settings.json)
   pi install -l "/ruta/absoluta/a/electro-study-shell"    # solo este proyecto (.pi/settings.json)
   pi -e "/ruta/absoluta/a/electro-study-shell"            # probarlo sin instalar, una invocación
   ```
3. Arranca `pi` **desde este directorio**. Verificación del arranque: el diagnóstico anuncia las 7 skills, y el autocompletado de `/` ofrece `/tutor`, `/redactor`, `/revisor`.
4. Primera prueba: `/tutor explícame la potencia trifásica`.

Notas de arranque:

- Instalado por ruta local, el paquete se carga **desde este repo sin copia**: cualquier edición de skills o prompts aplica tras `/reload` o al reiniciar `pi`.
- Trabaja desde este directorio si quieres citas del corpus: en otro proyecto el paquete funciona, pero el corpus no existe allí y todo valor normativo queda marcado `[VERIFICAR: ITC-BT-XX]`.
- `memoria-aprendizaje` necesita [Engram](https://github.com/Gentleman-Programming/engram) instalado y conectado por MCP (`engram setup <agente>`); sin él, el resto funciona y esta skill avisa.

## Cómo se usa

No hay comandos propios: las peticiones se enrutan por intención, y los tres prompts se vuelcan como comandos de rol.

| Pides | Se activa |
| --- | --- |
| Memoria técnica, memoria de diseño, documento de instalación | `memoria-tecnica-electrica` |
| Diagrama, flujo, secuencia, bloques, GRAFCET aproximado | `mermaid-diagramas` |
| «Explícame», repaso, ejercicios, test | `tutor-electrotecnia` |
| Comprobar secciones, caídas de tensión, protecciones | `revisor-calculos-electricos` |
| Crear o editar planillas, .xlsx, .csv, cuadros de cargas, presupuestos | `hojas-de-calculo` |
| Leer, extraer o resumir un PDF; crear o exportar a PDF | `pdf-leer-crear` |
| Guardar o recuperar aprendizajes, errores y correcciones | `memoria-aprendizaje` |

Prompts como comandos: `/tutor [tema]`, `/redactor [documento o datos]`, `/revisor [cálculos o sección]`. Se puede forzar una skill con `/skill:nombre` (p. ej. `/skill:revisor-calculos-electricos`).

Marcadores del contrato — qué significan en las respuestas del agente:

| Marcador | Significado |
| --- | --- |
| `[FUENTE: md/ITC-BT-XX.md §Y]` | Texto normativo citado del corpus; `[FUENTE: tablas/_v2/…]` para valores numéricos verificados |
| `[VERIFICAR: ITC-BT-XX]` | Valor o artículo pendiente de comprobar en la ITC vigente; nunca se usa como definitivo |
| `[POR COMPLETAR: campo]` | Dato del titular, centro, alumno o instalación que el agente no inventa |

Reglas de fondo (detalladas en `AGENTS.md` y en cada `SKILL.md`):

- Todo cálculo muestra fórmula, datos con unidades, sustitución y resultado, y pasa por `revisor-calculos-electricos` antes de darse por válido.
- Los límites normativos se toman del corpus si existe (citando `[FUENTE]`); si no, `[VERIFICAR]`. Nunca de memoria.
- La salida es Markdown: el alumno la vuelca a su plantilla (Google Docs o .docx).

## Contenido

| Skill | Para qué |
| --- | --- |
| `memoria-tecnica-electrica` | Esqueleto y redacción de memorias técnicas de instalaciones eléctricas de baja tensión |
| `mermaid-diagramas` | Diagramas Mermaid válidos (flujos, bloques, secuencias, estados) con validación `mmdc` |
| `tutor-electrotecnia` | Explicaciones por niveles, ejercicios y repaso |
| `revisor-calculos-electricos` | Revisión independiente de secciones, caídas de tensión y protecciones |
| `hojas-de-calculo` | Crear y editar .xlsx/.csv con fórmulas vivas, recálculo y modelos eléctricos |
| `pdf-leer-crear` | Leer y extraer de PDF (texto, tablas, escaneados) y crear PDF desde Markdown |
| `memoria-aprendizaje` | Guarda y recupera aprendizajes, errores y correcciones en Engram, con convención de claves y plantillas |

## Estructura

```text
skills/{nombre}/SKILL.md     # contrato de runtime (6 secciones)
skills/{nombre}/assets/      # plantillas y ejemplos
skills/{nombre}/references/  # teoría y fórmulas
prompts/                     # roles: tutor, redactor, revisor
references/rebt_salida/      # corpus normativo REBT (ver sección siguiente)
scripts/validate-skills.sh   # valida frontmatter, secciones y referencias
scripts/validate-mermaid.sh  # valida diagramas con mmdc
scripts/recalc-xlsx.sh       # recalcula un .xlsx y lista errores de fórmula
scripts/pdf-info.sh          # inventario de un PDF
scripts/md-to-pdf.py         # Markdown sencillo a PDF
scripts/extraer-tablas-rebt.py  # re-extrae las tablas del corpus desde el XML
```

## Dependencias

Scripts: Python 3 con `openpyxl`, `pypdf`, `reportlab`, `pdfplumber` y `defusedxml` (venv del proyecto en `.venv/`).

Herramientas de sistema — estado real hoy:

| Herramienta | Estado | Si la quieres |
| --- | --- | --- |
| `magick`, `tesseract` (OCR) | instaladas | — |
| poppler (`pdftotext`/`pdftoppm`) | no instalado | `brew install poppler` |
| LibreOffice (`soffice`, recalcular planillas) | no instalado | cask de LibreOffice |
| `mmdc` (validar Mermaid) | no instalado | `npm i -g @mermaid-js/mermaid-cli` |

Las skills degradan con aviso cuando falta una herramienta; ninguno de los pendientes bloquea el arranque.

## Corpus normativo (`references/rebt_salida/`)

Texto íntegro del REBT y sus ITC (BOE-A-2002-18099) descargado de la API de datos abiertos del BOE. **El texto normativo (`md/`) es citable; la capa numérica no se usa sin verificar.**

| Capa | Contenido | Estado |
| --- | --- | --- |
| `cache/*.xml` | 99 respuestas de la API, con el HTML intacto | fuente de verdad para las tablas |
| `md/*.md` | 54 archivos: texto normativo por ITC | citable: `[FUENTE: md/ITC-BT-XX.md §Y]` |
| `imgs/*.png` | 63 escaneos; los 73 `![imagen]` de los md apuntan a la ruta local (`../imgs/…`) | sin dependencia de red |
| `tablas/*.csv` | 73 CSV de la extracción anterior | **solo referencia histórica**: aplastaba subfilas, `colspan`/`rowspan` y descartaba `<tfoot>` |
| `tablas/_v2/*.csv` | 73 tablas re-extraídas desde el XML | **verificado: 0 celdas del XML ausentes del CSV**, 27 tablas con subfilas expandidas, 0 filas irregulares |
| `tablas/_verificadas/` | transcripción de la única tabla que el BOE solo publica como imagen | ver `tablas/_verificadas/ITC-BT-19_tabla1-PROCEDENCIA.md` |

Extracción reproducible:

```sh
.venv/bin/python scripts/extraer-tablas-rebt.py            # extrae a tablas/_v2
.venv/bin/python scripts/extraer-tablas-rebt.py --verify  # comprueba contra el XML (exit 0 = 0 celdas perdidas)
```

Cada tabla de `_v2` declara su procedencia en `tablas/_v2/_manifest.json` (bloque y tabla de origen del XML).

**Regla de uso de la capa numérica**: los CSV de `_v2` provienen del HTML oficial, pero las combinaciones (columna ↔ método de instalación ↔ aislamiento) deben leerse de la cabecera transcrita, no asumirse. La correspondencia cabecera-columna de ITC-BT-19 Tabla 1 queda `[VERIFICAR: UNE 20.460-5-523]`. Cualquier valor normativo que no esté en el corpus se marca `[VERIFICAR: ITC-BT-XX]`, nunca se inventa.

## Pendiente

- Confirmar la correspondencia cabecera-columna de ITC-BT-19 Tabla 1 contra **UNE 20.460-5-523** (el escaneo solapa su propia cabecera; los valores numéricos sí están verificados — primer pase visual + segundo pase OCR con `tesseract`; ver `tablas/_verificadas/ITC-BT-19_tabla1-PROCEDENCIA.md`).
- Los `md/*.md` duplican su árbol de secciones como índice y luego como contenido (~2× tokens): deduplicar si se usan para RAG.

## Licencia

MIT. Inspirado en el contrato de skills de `gentle-shell` / `gentle-pi` (MIT); no incluye su código ni sus marcas.
