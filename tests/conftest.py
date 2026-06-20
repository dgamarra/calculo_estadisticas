from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def csv_factory(tmp_path: Path) -> Generator[Any, Any, Any]:
    """Factory fixture: crea un archivo CSV en tmp_path y devuelve su ruta."""

    def _crear(contenido: str, nombre: str = "test.csv") -> str:
        ruta = tmp_path / nombre
        ruta.write_text(contenido, encoding="utf-8")
        return str(ruta)

    yield _crear


@pytest.fixture
def csv_valores_nulos(csv_factory: Any) -> str:
    """CSV con valores nulos (; como delimitador)."""
    return csv_factory(
        "nombre;edad;salario\n"
        "Alice;30;50000\n"
        "Bob;25;45000\n"
        "Charlie;35;\n"
        "Diana;28;52000\n",
        "nulos.csv",
    )


@pytest.fixture
def csv_comas(csv_factory: Any) -> str:
    """CSV con coma como delimitador."""
    return csv_factory(
        "a,b,c\n1.5,2.5,3.5\n4.5,5.5,6.5\n", "comas.csv"
    )


@pytest.fixture
def csv_tab(csv_factory: Any) -> str:
    """CSV con tabulación como delimitador."""
    return csv_factory(
        "x\ty\tz\n10\t20\t30\n40\t50\t60\n", "tab.csv"
    )


@pytest.fixture
def csv_vacio(csv_factory: Any) -> str:
    """Archivo CSV completamente vacío."""
    return csv_factory("", "vacio.csv")


@pytest.fixture
def csv_solo_header(csv_factory: Any) -> str:
    """CSV con solo encabezados, sin datos."""
    return csv_factory("col1,col2,col3\n", "solo_header.csv")


@pytest.fixture
def csv_mixto(csv_factory: Any) -> str:
    """CSV con columnas numéricas y de texto."""
    return csv_factory(
        "nombre,edad,ciudad\n"
        "Alice,30,Madrid\n"
        "Bob,25,Barcelona\n"
        "Charlie,35,Valencia\n",
        "mixto.csv",
    )


@pytest.fixture
def csv_una_fila(csv_factory: Any) -> str:
    """CSV con una sola fila de datos."""
    return csv_factory("x,y\n42,99\n", "una_fila.csv")


@pytest.fixture
def csv_constante(csv_factory: Any) -> str:
    """CSV con valores constantes en todas las filas."""
    return csv_factory("a,b\n5,10\n5,10\n5,10\n", "constante.csv")
