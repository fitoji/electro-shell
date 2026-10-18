---
name: memoria-tecnica-electrica
description: "Trigger: memoria técnica, memoria de diseño, memoria eléctrica, documento de instalación BT, REBT. Redacta y estructura memorias técnicas de instalaciones eléctricas de baja tensión en español."
license: MIT
metadata:
  author: electro-study-shell
  version: "0.1"
---

## Activation Contract
- Activar cuando se pida redactar, revisar o estructurar una memoria técnica eléctrica de BT.
- No activar para explicaciones teóricas (usar `tutor-electrotecnia`) ni para solo comprobar cálculos (usar `revisor-calculos-electricos`).

## Hard Rules
- No inventar datos del titular, centro, alumno, emplazamiento ni potencias: usar `[POR COMPLETAR: campo]`.
- No citar artículos ni valores normativos de memoria: buscarlos en el corpus del proyecto `references/rebt_salida/` (texto en `md/ITC-BT-XX.md`, valores en `tablas/_v2/`) y citar `[FUENTE: …]`; lo que no esté, `[VERIFICAR: ITC-BT-XX]`.
- Todo cálculo incluido debe pasar por `revisor-calculos-electricos`.
- Salida en Markdown; el usuario la vuelca a su plantilla (Google Docs o .docx).

## Decision Gates
| Situación | Acción |
| --- | --- |
| Faltan datos de potencia, tensión o longitudes | Preguntar o dejar marcador; no suponer |
| El usuario aporta plantilla propia | Respetar su orden y cabecera; no imponer `assets/plantilla-memoria.md` |
| Instalación que podría requerir proyecto | Avisar y remitir a la ITC-BT-04 vigente |
| Pide esquema unifilar normalizado | Ofrecer diagrama de bloques Mermaid y avisar de la limitación |

## Execution Steps
1. Confirmar tipo de instalación, tensión, potencia prevista y datos disponibles; recuperar con `memoria-aprendizaje` las preferencias de estilo del usuario y el estado del proyecto.
2. Partir de `assets/plantilla-memoria.md` y `references/estructura-rebt.md`.
3. Redactar sección a sección; cada cálculo con fórmula, datos, sustitución y resultado.
4. Marcar pendientes con `[POR COMPLETAR]` y `[VERIFICAR]`.
5. Enviar cálculos al revisor y corregir discrepancias.
6. Listar pendientes al final y guardar el estado del proyecto y las correcciones de estilo con `memoria-aprendizaje`.

## Output Contract
- Documento Markdown con índice y secciones numeradas.
- Lista final de marcadores pendientes.
- Cálculos revisados o indicados como no revisados.
- Riesgos residuales y suposiciones declaradas.

## References
- `assets/plantilla-memoria.md`
- `references/estructura-rebt.md`
- Corpus normativo del proyecto: `references/rebt_salida/md/` y `references/rebt_salida/tablas/_v2/`
