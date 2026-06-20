import csv
from typing import Optional

import numpy as np
import pandas as pd


def analizar_csv(
    ruta: str,
    eliminar_nulos: bool = True,
    columnas: Optional[list[str]] = None,
) -> dict[str, dict[str, float]]:
    """Lee un CSV, calcula estadísticas descriptivas de columnas numéricas
    y retorna los resultados en un diccionario anidado.

    Args:
        ruta: Ruta al archivo CSV.
        eliminar_nulos: Si True, elimina filas con valores nulos.
                        Si False, imputa con la mediana de cada columna.
        columnas: Lista opcional de columnas a analizar.
                  Si no se especifica, se analizan todas las columnas numéricas.

    Returns:
        Diccionario donde cada clave es el nombre de una columna y su valor
        es otro diccionario con: media, mediana, desviacion_estandar,
        percentil_25 y percentil_75.

    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta indicada.
        pd.errors.EmptyDataError: Si el archivo CSV está vacío.
        ValueError: Si alguna columna solicitada no existe o no es numérica.
    """
    try:
        with open(ruta, encoding="utf-8") as f:
            contenido = f.read(2048)
            if not contenido.strip():
                raise pd.errors.EmptyDataError(f"El archivo está vacío: {ruta}")
            dialecto = csv.Sniffer().sniff(contenido)
            f.seek(0)
            df = pd.read_csv(f, sep=dialecto.delimiter)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    except pd.errors.EmptyDataError:
        raise

    if df.empty:
        raise pd.errors.EmptyDataError(f"El archivo no contiene datos: {ruta}")

    if eliminar_nulos:
        df = df.dropna()
    else:
        df = df.fillna(df.median(numeric_only=True))

    columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

    if columnas is not None:
        for col in columnas:
            if col not in df.columns:
                raise ValueError(f"La columna '{col}' no existe en el archivo.")
            if col not in columnas_numericas:
                raise ValueError(
                    f"La columna '{col}' no es numérica. "
                    f"Columnas numéricas disponibles: {columnas_numericas}"
                )
        cols_final: list[str] = columnas
    else:
        if not columnas_numericas:
            raise ValueError(
                "No se encontraron columnas numéricas en el archivo."
            )
        cols_final = columnas_numericas

    resultado: dict[str, dict[str, float]] = {}
    for col in cols_final:
        serie = df[col]
        resultado[col] = {
            "media": float(serie.mean()),
            "mediana": float(serie.median()),
            "desviacion_estandar": float(serie.std()),
            "percentil_25": float(serie.quantile(0.25)),
            "percentil_75": float(serie.quantile(0.75)),
        }

    return resultado


if __name__ == "__main__":
    import sys

    ruta = sys.argv[1] if len(sys.argv) > 1 else "datos.csv"
    resultado = analizar_csv(ruta)
    for col, stats in resultado.items():
        print(f"{col}: {stats}")
