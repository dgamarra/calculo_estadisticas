import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


def leer_lineas(ruta: str | Path) -> list[str]:
    """Lee todas las líneas no vacías de un archivo.

    Args:
        ruta: Ruta al archivo de texto.

    Returns:
        Lista de líneas sin espacios en blanco al inicio/final.

    Raises:
        FileNotFoundError: Si el archivo no existe.
    """
    ruta = Path(ruta)
    with open(ruta, encoding="utf-8") as f:
        return [linea.strip() for linea in f if linea.strip()]


def parsear_linea(linea: str) -> Optional[dict[str, Any]]:
    """Convierte una línea CSV de 3 campos en un diccionario.

    Formato esperado: nombre,num,edad

    Args:
        linea: Línea de texto con campos separados por coma.

    Returns:
        Diccionario con claves 'name', 'num' y 'age', o None si la línea
        no tiene el formato esperado.
    """
    partes = linea.split(",")
    if len(partes) != 3:
        logger.warning("Línea ignorada (se esperaban 3 campos): %s", linea)
        return None
    try:
        nombre = partes[0].strip()
        num = float(partes[1])
        edad = int(partes[2])
    except ValueError as exc:
        logger.warning("Línea ignorada (error de conversión): %s — %s", linea, exc)
        return None
    return {"name": nombre, "num": num, "age": edad}


def procesar_archivo(ruta: str | Path) -> list[dict[str, Any]]:
    """Lee un archivo CSV con formato nombre,num,edad y devuelve una lista
    de registros válidos.

    Args:
        ruta: Ruta al archivo de entrada.

    Returns:
        Lista de diccionarios con los registros parseados correctamente.

    Raises:
        FileNotFoundError: Si el archivo no existe.
    """
    lineas = leer_lineas(ruta)
    logger.info("Procesando archivo: %s (%d líneas)", ruta, len(lineas))

    registros: list[dict[str, Any]] = []
    for linea in lineas:
        registro = parsear_linea(linea)
        if registro is not None:
            registros.append(registro)

    logger.info("Registros válidos: %d de %d", len(registros), len(lineas))
    return registros
