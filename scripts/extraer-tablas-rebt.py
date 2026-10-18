#!/usr/bin/env python3
"""Extrae las tablas del corpus REBT desde cache/*.xml a tablas/_v2/.

El corpus guarda en cache/ las respuestas de la API de datos abiertos del BOE,
donde las tablas conservan su HTML original (thead/tbody/tr/td) con rowspan,
colspan, superindices e imagenes. El extractor anterior las aplastaba porque un
mismo td puede contener varios p, es decir subfilas.

Uso:
    python3 scripts/extraer-tablas-rebt.py             # extrae a tablas/_v2/
    python3 scripts/extraer-tablas-rebt.py --verify     # ademas compara con tablas/
    python3 scripts/extraer-tablas-rebt.py --dry-run    # solo informe, no escribe

Salida: tablas/_v2/{grupo}_t{NN}.csv + tablas/_v2/_manifest.json

Dependencia: defusedxml (venv del proyecto)
    python3 -m venv .venv && .venv/bin/pip install defusedxml
"""

import argparse
import csv
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(RAIZ, "references", "rebt_salida")
CACHE = os.path.join(CORPUS, "cache")
INDICE = os.path.join(CORPUS, "indice.json")
SALIDA = os.path.join(CORPUS, "tablas", "_v2")
TABLAS_VIEJAS = os.path.join(CORPUS, "tablas")

SUPERSCRITOS = {
    "0": "\u2070", "1": "\u00b9", "2": "\u00b2", "3": "\u00b3", "4": "\u2074",
    "5": "\u2075", "6": "\u2076", "7": "\u2077", "8": "\u2078", "9": "\u2079",
    "-": "\u207b", "+": "\u207a",
}

RE_IMG = re.compile(r"/([^/]+\.(?:png|jpg|jpeg|gif))$")


class ErrorCorpus(Exception):
    """Fallo de lectura o escritura del corpus."""


# --------------------------------------------------------------------------
# E/S con contexto
# --------------------------------------------------------------------------

def cargar_xml(ruta):
    """Parsea un XML del corpus con defusedxml.

    El corpus viene de la API del BOE pero se trata como entrada no confiable:
    defusedxml rechaza DTD, entidades externas y expansion de entidades.
    """
    try:
        with open(ruta, "rb") as fh:
            crudo = fh.read()
    except OSError as exc:
        raise ErrorCorpus(f"no se pudo leer {ruta}: {exc}") from exc

    try:
        from defusedxml.ElementTree import fromstring
    except ImportError as exc:
        raise ErrorCorpus(
            "falta defusedxml; instalar con: .venv/bin/pip install defusedxml"
        ) from exc

    try:
        return fromstring(crudo)
    except ET.ParseError as exc:
        raise ErrorCorpus(f"XML invalido en {ruta}: {exc}") from exc
    except Exception as exc:  # noqa: BLE001  (defusedxml rechaza DTD y entidades)
        raise ErrorCorpus(f"XML rechazado en {ruta}: {exc}") from exc


def leer_json(ruta):
    try:
        with open(ruta, encoding="utf-8") as fh:
            return json.load(fh)
    except OSError as exc:
        raise ErrorCorpus(f"no se pudo leer {ruta}: {exc}") from exc
    except ValueError as exc:
        raise ErrorCorpus(f"JSON invalido en {ruta}: {exc}") from exc


def escribir_json(ruta, datos):
    try:
        with open(ruta, "w", encoding="utf-8") as fh:
            json.dump(datos, fh, ensure_ascii=False, indent=2)
    except OSError as exc:
        raise ErrorCorpus(f"no se pudo escribir {ruta}: {exc}") from exc


def escribir_csv(ruta, filas):
    try:
        with open(ruta, "w", encoding="utf-8", newline="") as fh:
            escritor = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
            for fila in filas:
                escritor.writerow(fila)
    except OSError as exc:
        raise ErrorCorpus(f"no se pudo escribir {ruta}: {exc}") from exc


def asegurar_directorio(ruta):
    try:
        os.makedirs(ruta, exist_ok=True)
    except OSError as exc:
        raise ErrorCorpus(f"no se pudo crear {ruta}: {exc}") from exc


def medir(ruta):
    """Devuelve (filas, columnas_max, filas_irregulares)."""
    try:
        with open(ruta, encoding="utf-8", newline="") as fh:
            filas = list(csv.reader(fh))
    except OSError as exc:
        raise ErrorCorpus(f"no se pudo leer {ruta}: {exc}") from exc
    if not filas:
        return 0, 0, 0
    ancho = max(len(f) for f in filas)
    irregulares = sum(1 for f in filas if len(f) != ancho)
    return len(filas), ancho, irregulares


def inventario_viejas():
    viejas = {}
    try:
        nombres = os.listdir(TABLAS_VIEJAS)
    except OSError:
        return viejas
    for nombre in nombres:
        if nombre.endswith(".csv") and not nombre.startswith("_"):
            viejas[nombre[:-4]] = os.path.join(TABLAS_VIEJAS, nombre)
    return viejas


# --------------------------------------------------------------------------
# Texto de celda
# --------------------------------------------------------------------------

def texto_inline(nodo, imagenes):
    """Texto de un nodo, expandiendo sup, sub e img (esta ultima como marcador)."""
    partes = []
    if nodo.text:
        partes.append(nodo.text)
    for hijo in nodo:
        if hijo.tag == "sup":
            interior = "".join(hijo.itertext())
            if not interior.strip():
                partes.append(" ")
            else:
                partes.append("".join(
                    SUPERSCRITOS.get(caracter, caracter) for caracter in interior.strip()))
        elif hijo.tag == "sub":
            interior = "".join(hijo.itertext()).strip()
            partes.append("_" + interior)
        elif hijo.tag == "img":
            origen = hijo.get("src", "")
            coincidencia = RE_IMG.search(origen)
            nombre = (coincidencia.group(1) if coincidencia
                      else os.path.basename(origen)) or "imagen"
            imagenes.append(nombre)
            partes.append(f"[img:{nombre}]")
        elif hijo.tag == "br":
            partes.append(" ")
        else:
            partes.append(texto_inline(hijo, imagenes))
        if hijo.tail:
            partes.append(hijo.tail)
    return "".join(partes)


def normalizar(texto):
    texto = texto.replace("\u00a0", " ")
    texto = re.sub(r"[ \t\r\n]+", " ", texto)
    return texto.strip()


def parrafos_de_celda(celda, imagenes):
    """Subfilas de una celda: un p por subfila. Sin p, todo el texto es una."""
    parrafos = celda.findall("p")
    if not parrafos:
        return [normalizar(texto_inline(celda, imagenes))]
    return [normalizar(texto_inline(p, imagenes)) for p in parrafos]


# --------------------------------------------------------------------------
# Rejilla con spans y subfilas
# --------------------------------------------------------------------------

class Celda:
    """Celda de la rejilla fisica, con su fila de origen y sus subfilas."""

    __slots__ = ("parrafos", "origen_fila", "rowspan", "colspan")

    def __init__(self, parrafos, origen_fila, rowspan, colspan):
        self.parrafos = parrafos
        self.origen_fila = origen_fila
        self.rowspan = rowspan
        self.colspan = colspan


def construir_rejilla(filas):
    """Aplica colspan y rowspan. Devuelve un dict (fila, col) -> Celda."""
    rejilla = {}
    for indice, tr in enumerate(filas):
        col = 0
        for celda in tr:
            if celda.tag not in ("td", "th"):
                continue
            while (indice, col) in rejilla:
                col += 1
            rowspan = int(celda.get("rowspan") or 1)
            colspan = int(celda.get("colspan") or 1)
            imagenes = []
            parrafos = parrafos_de_celda(celda, imagenes) or [""]
            objeto = Celda(parrafos, indice, rowspan, colspan)
            for desplazamiento_fila in range(rowspan):
                for desplazamiento_col in range(colspan):
                    rejilla[(indice + desplazamiento_fila, col + desplazamiento_col)] = objeto
            col += colspan
    return rejilla


def ancho_rejilla(rejilla):
    if not rejilla:
        return 0
    return max(col for _, col in rejilla) + 1


def parrafos_efectivos(celda, ancho):
    """Subfilas reales de una celda.

    Una celda que ocupa todo el ancho es una nota al pie, no una columna de
    subfilas: sus parrafos se unen en un solo valor.
    """
    if celda.colspan >= ancho and len(celda.parrafos) > 1:
        return [" ".join(p for p in celda.parrafos if p)]
    return celda.parrafos


def expandir_subfilas(rejilla, n_filas):
    """Abre cada fila fisica en tantas filas logicas como subfilas tenga.

    Las celdas con una sola subfila se repiten para que cada fila logica quede
    completa y sea consultable por si sola. Las celdas heredadas por rowspan no
    se repiten si aportan varias subfilas: ya se emitieron en su fila de origen.
    """
    ancho = ancho_rejilla(rejilla)
    alturas = {}
    for indice in range(n_filas):
        altura = 1
        for col in range(ancho):
            celda = rejilla.get((indice, col))
            if celda is not None and celda.origen_fila == indice:
                altura = max(altura, len(parrafos_efectivos(celda, ancho)))
        alturas[indice] = altura

    filas_logicas = []
    hubo_subfilas = False
    for indice in range(n_filas):
        altura = alturas[indice]
        if altura > 1:
            hubo_subfilas = True
        for desplazamiento in range(altura):
            fila = []
            for col in range(ancho):
                celda = rejilla.get((indice, col))
                if celda is None:
                    fila.append("")
                    continue
                parrafos = parrafos_efectivos(celda, ancho)
                heredada = celda.origen_fila != indice
                if len(parrafos) == 1:
                    fila.append(parrafos[0])
                elif heredada:
                    fila.append("")
                elif desplazamiento < len(parrafos):
                    fila.append(parrafos[desplazamiento])
                else:
                    fila.append("")
            filas_logicas.append(fila)
    return filas_logicas, hubo_subfilas, alturas


def fusionar_cabecera(filas_cabecera, ancho):
    """Aplana varias filas de cabecera en una etiqueta por columna."""
    etiquetas = []
    for col in range(ancho):
        partes = []
        for fila in filas_cabecera:
            valor = fila[col].strip() if col < len(fila) else ""
            if valor and (not partes or partes[-1] != valor):
                partes.append(valor)
        etiquetas.append(" | ".join(partes))
    return etiquetas


def tabla_desde_nodo(nodo_tabla):
    """Devuelve (filas_con_cabecera, hubo_subfilas, n_celdas_imagen).

    Incluye tfoot: las notas al pie de las tablas del BOE viven ahi y forman
    parte del contenido normativo que hay que conservar.
    """
    thead = nodo_tabla.find("thead")
    tbody = nodo_tabla.find("tbody")
    tfoot = nodo_tabla.find("tfoot")
    origen_cabecera = list(thead) if thead is not None else []
    if tbody is not None:
        origen_cuerpo = list(tbody)
    else:
        origen_cuerpo = nodo_tabla.findall("tr")
    if tfoot is not None:
        origen_cuerpo = origen_cuerpo + list(tfoot)
    filas_cabecera = [f for f in origen_cabecera if f.tag == "tr"]
    filas_cuerpo = [f for f in origen_cuerpo if f.tag == "tr"]

    todas = filas_cabecera + filas_cuerpo
    rejilla = construir_rejilla(todas)
    ancho = ancho_rejilla(rejilla)
    filas_logicas, hubo_subfilas, alturas = expandir_subfilas(rejilla, len(todas))

    n_logicas_cabecera = sum(alturas[i] for i in range(len(filas_cabecera)))
    if filas_cabecera and n_logicas_cabecera:
        encabezados = fusionar_cabecera(filas_logicas[:n_logicas_cabecera], ancho)
        cuerpo = filas_logicas[n_logicas_cabecera:]
    else:
        encabezados = [f"col{col + 1}" for col in range(ancho)]
        cuerpo = filas_logicas

    n_imagenes = sum(1 for fila in filas_logicas for celda in fila
                     if celda.startswith("[img:"))
    return [encabezados] + cuerpo, hubo_subfilas, n_imagenes


# --------------------------------------------------------------------------
# Corpus
# --------------------------------------------------------------------------

def leer_indice():
    indice = leer_json(INDICE)
    grupos = {}
    for bloque in indice["bloques"]:
        grupos.setdefault(bloque["grupo"], []).append(
            (bloque.get("n", 0), bloque["id"]))
    for identificadores in grupos.values():
        identificadores.sort()
    orden = []
    vistos = set()
    for bloque in indice["bloques"]:
        if bloque["grupo"] not in vistos:
            vistos.add(bloque["grupo"])
            orden.append(bloque["grupo"])
    return grupos, orden


def version_vigente(bloque):
    """Version consolidada: la ultima por fecha de vigencia."""
    versiones = bloque.findall(".//version")
    if not versiones:
        return bloque

    def clave(version):
        return (version.get("fecha_vigencia") or "",
                version.get("fecha_publicacion") or "")

    return sorted(versiones, key=clave)[-1]


def extraer(escribir=True):
    grupos, orden = leer_indice()
    if escribir:
        asegurar_directorio(SALIDA)
    manifiesto = []
    problemas = []

    for grupo in orden:
        contador = 0
        for _, bloque_id in grupos[grupo]:
            ruta = os.path.join(CACHE, f"bloque_{bloque_id}.xml")
            if not os.path.exists(ruta):
                problemas.append(
                    f"falta cache/bloque_{bloque_id}.xml (grupo {grupo})")
                continue
            try:
                raiz_xml = cargar_xml(ruta)
            except ErrorCorpus as exc:
                problemas.append(f"bloque_{bloque_id}.xml descartado: {exc}")
                continue
            bloque = raiz_xml.find(".//bloque")
            if bloque is None:
                problemas.append(f"bloque_{bloque_id}.xml sin nodo bloque")
                continue
            nodo = version_vigente(bloque)
            for tabla in nodo.iter("table"):
                contador += 1
                nombre = f"{grupo}_t{contador:02d}"
                try:
                    filas, subfilas, n_imagenes = tabla_desde_nodo(tabla)
                except (TypeError, ValueError) as exc:
                    problemas.append(f"{nombre}: no se pudo leer ({exc})")
                    continue
                ancho = max(len(fila) for fila in filas) if filas else 0
                irregulares = sum(1 for fila in filas if len(fila) != ancho)
                vacias = sum(1 for fila in filas[1:] for celda in fila
                             if not celda.strip())
                perdidas = celdas_perdidas(tabla, filas)
                if perdidas:
                    problemas.append(
                        f"{nombre}: {len(perdidas)} celdas del XML sin llegar "
                        f"al CSV (p.ej. {perdidas[0]!r})")
                if escribir:
                    escribir_csv(os.path.join(SALIDA, f"{nombre}.csv"), filas)
                manifiesto.append({
                    "tabla": nombre,
                    "grupo": grupo,
                    "bloque": bloque_id,
                    "origen": f"cache/bloque_{bloque_id}.xml",
                    "filas": max(len(filas) - 1, 0),
                    "columnas": ancho,
                    "subfilas_expandidas": subfilas,
                    "imagenes_en_celda": n_imagenes,
                    "filas_irregulares": irregulares,
                    "celdas_vacias": vacias,
                    "celdas_perdidas": len(perdidas),
                    "archivo": f"{nombre}.csv",
                })
                if irregulares:
                    problemas.append(
                        f"{nombre}: {irregulares} filas con ancho != {ancho}")

    if escribir:
        escribir_json(os.path.join(SALIDA, "_manifest.json"),
                      {"total": len(manifiesto), "tablas": manifiesto})
    return manifiesto, problemas


# --------------------------------------------------------------------------
# Verificacion
# --------------------------------------------------------------------------

RE_NUM = re.compile(r"\d+(?:[.,]\d+)?")


def celdas_perdidas(nodo_tabla, filas):
    """Celdas del XML cuyo texto no aparece en el CSV extraido.

    Es la verificacion contra la fuente: si una celda del XML no llega al CSV,
    el extractor perdio contenido. No depende de la extraccion anterior.
    """
    texto_csv = "\n".join(",".join(fila) for fila in filas)
    perdidas = []
    for celda in nodo_tabla.iter():
        if celda.tag not in ("td", "th"):
            continue
        imagenes = []
        for parrafo in parrafos_de_celda(celda, imagenes):
            if parrafo and parrafo not in texto_csv:
                perdidas.append(parrafo[:80])
    return perdidas


def verificar(manifiesto):
    viejas = inventario_viejas()
    nuevas = {tabla["tabla"]: tabla for tabla in manifiesto}

    solo_viejas = sorted(set(viejas) - set(nuevas))
    solo_nuevas = sorted(set(nuevas) - set(viejas))
    ambas = sorted(set(viejas) & set(nuevas))

    perdidas = [(t["tabla"], t["celdas_perdidas"])
                for t in manifiesto if t["celdas_perdidas"]]

    print("=" * 70)
    print("VERIFICACION  tablas/_v2  vs  tablas/")
    print("=" * 70)
    print(f"Tablas en _v2                 : {len(nuevas)}")
    print(f"Tablas en tablas/ (anteriores): {len(viejas)}")
    print(f"En ambas                      : {len(ambas)}")
    print(f"Solo en _v2 (nuevas)          : {len(solo_nuevas)}")
    print(f"Solo en tablas/ (sin par)     : {len(solo_viejas)}")
    print()
    print("Cobertura contra la fuente (cache/*.xml):")
    print(f"Tablas con celdas del XML que no llegan al CSV: {len(perdidas)}")
    for nombre, cuantas in perdidas[:15]:
        print(f"  {nombre:<22} {cuantas} celdas")
    if not perdidas:
        print("  ninguna: toda celda del XML esta representada en el CSV")


    if solo_nuevas:
        print()
        print(f"Tablas recuperadas que antes no existian ({len(solo_nuevas)}):")
        for nombre in solo_nuevas:
            tabla = nuevas[nombre]
            print(f"  {nombre:<22} {tabla['filas']:2d} fil x {tabla['columnas']:2d} col"
                  f"   ({tabla['origen']})")
    if solo_viejas:
        print()
        print("CSV anteriores sin correspondencia en _v2:")
        for nombre in solo_viejas:
            print(f"  {nombre}")

    con_subfilas = [t["tabla"] for t in manifiesto if t["subfilas_expandidas"]]
    con_imagenes = [t["tabla"] for t in manifiesto if t["imagenes_en_celda"]]
    irregulares = [t["tabla"] for t in manifiesto if t["filas_irregulares"]]
    print()
    print(f"Tablas con subfilas expandidas : {len(con_subfilas)}")
    listado = ", ".join(con_imagenes[:8]) if con_imagenes else ""
    print(f"Tablas con celdas-imagen       : {len(con_imagenes)}  {listado}")
    print(f"Tablas con filas irregulares   : {len(irregulares)}")
    for nombre in irregulares[:10]:
        print(f"  {nombre}")
    return perdidas, solo_nuevas


def main():
    parser = argparse.ArgumentParser(
        description="Extrae las tablas del corpus REBT desde cache/*.xml.")
    parser.add_argument("--verify", action="store_true",
                        help="compara la extraccion con tablas/ existente")
    parser.add_argument("--dry-run", action="store_true",
                        help="no escribe CSV, solo informa")
    argumentos = parser.parse_args()

    try:
        manifiesto, problemas = extraer(escribir=not argumentos.dry_run)
    except ErrorCorpus as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if argumentos.dry_run:
        print(f"dry-run: {len(manifiesto)} tablas detectadas, nada escrito")
    else:
        destino = os.path.relpath(SALIDA, RAIZ)
        print(f"Extraidas {len(manifiesto)} tablas a {destino}")

    if problemas:
        print(f"\nAvisos ({len(problemas)}):")
        for aviso in problemas[:20]:
            print(f"  {aviso}")
        if len(problemas) > 20:
            print(f"  ... y {len(problemas) - 20} mas")

    if argumentos.verify:
        print()
        try:
            perdidas, _ = verificar(manifiesto)
        except ErrorCorpus as exc:
            print(f"Error en la verificacion: {exc}", file=sys.stderr)
            return 1
        if perdidas:
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
