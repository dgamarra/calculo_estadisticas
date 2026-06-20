import math

import numpy as np
import pandas as pd
import pytest

from calculo_estadisticas.analisis import analizar_csv


# =============================================================================
# Casos felices — delimitadores
# =============================================================================

class TestDelimitadores:
    def test_delimitador_coma(self, csv_comas: str) -> None:
        resultado = analizar_csv(csv_comas)
        assert "a" in resultado
        assert resultado["a"]["media"] == 3.0
        assert resultado["a"]["mediana"] == 3.0
        assert resultado["b"]["media"] == 4.0

    def test_delimitador_punto_coma(self, csv_valores_nulos: str) -> None:
        resultado = analizar_csv(csv_valores_nulos, eliminar_nulos=True)
        assert "edad" in resultado
        assert resultado["edad"]["media"] == pytest.approx(27.6667, rel=1e-3)

    def test_delimitador_tabulacion(self, csv_tab: str) -> None:
        resultado = analizar_csv(csv_tab)
        assert resultado["x"]["media"] == 25.0
        assert resultado["y"]["percentil_25"] == 27.5
        assert resultado["z"]["percentil_75"] == 52.5


# =============================================================================
# Casos felices — opciones de la función
# =============================================================================

class TestOpciones:
    def test_columnas_especificas(self, csv_valores_nulos: str) -> None:
        resultado = analizar_csv(csv_valores_nulos, columnas=["edad"])
        assert list(resultado.keys()) == ["edad"]
        assert resultado["edad"]["mediana"] == 28.0

    def test_eliminar_nulos(self, csv_valores_nulos: str) -> None:
        resultado = analizar_csv(csv_valores_nulos, eliminar_nulos=True)
        # Charlie (fila con nulo) queda excluida → 3 filas
        assert resultado["edad"]["media"] == pytest.approx(27.6667, rel=1e-3)

    def test_imputar_nulos(self, csv_valores_nulos: str) -> None:
        resultado = analizar_csv(csv_valores_nulos, eliminar_nulos=False)
        # La mediana de salario [45000, 50000, 52000] = 50000
        # se imputa en Charlie, luego media = (50000+45000+50000+52000)/4 = 49250
        assert resultado["salario"]["media"] == 49250.0
        assert resultado["salario"]["mediana"] == 50000.0

    def test_todas_las_columnas_numericas(self, csv_comas: str) -> None:
        resultado = analizar_csv(csv_comas)
        assert set(resultado.keys()) == {"a", "b", "c"}
        assert all(isinstance(v, float) for stats in resultado.values() for v in stats.values())


# =============================================================================
# Casos borde
# =============================================================================

class TestCasosBorde:
    def test_archivo_vacio(self, csv_vacio: str) -> None:
        with pytest.raises(pd.errors.EmptyDataError, match="vacío"):
            analizar_csv(csv_vacio)

    def test_archivo_solo_header(self, csv_solo_header: str) -> None:
        with pytest.raises(pd.errors.EmptyDataError, match="vacío|no contiene datos"):
            analizar_csv(csv_solo_header)

    def test_sin_columnas_numericas(self, csv_factory: Any) -> None:
        ruta = csv_factory("a,b\nx,y\n", "solo_texto.csv")
        with pytest.raises(ValueError, match="No se encontraron columnas numéricas"):
            analizar_csv(ruta)

    def test_una_sola_fila(self, csv_una_fila: str) -> None:
        resultado = analizar_csv(csv_una_fila)
        assert resultado["x"]["media"] == 42.0
        assert resultado["y"]["mediana"] == 99.0
        assert math.isnan(resultado["x"]["desviacion_estandar"])

    def test_columna_constante(self, csv_constante: str) -> None:
        resultado = analizar_csv(csv_constante)
        assert resultado["a"]["desviacion_estandar"] == 0.0
        assert resultado["a"]["media"] == 5.0
        assert resultado["a"]["percentil_25"] == 5.0
        assert resultado["a"]["percentil_75"] == 5.0

    def test_sin_nulos_en_csv_normal(self, csv_comas: str) -> None:
        """Verifica que un CSV sin nulos retorne valores numéricos correctos."""
        resultado = analizar_csv(csv_comas, eliminar_nulos=True)
        assert resultado["a"]["media"] == 3.0

    def test_columnas_mixtas_solo_numericas(self, csv_mixto: str) -> None:
        """Solo debe analizar columnas numéricas, ignorando las de texto."""
        resultado = analizar_csv(csv_mixto)
        assert set(resultado.keys()) == {"edad"}
        assert "nombre" not in resultado
        assert "ciudad" not in resultado

    def test_todos_los_valores_nulos(self, csv_factory: Any) -> None:
        """Con todas las filas nulas y drop, el DataFrame queda vacío
        pero las columnas preservan dtype numérico; los stats son NaN."""
        ruta = csv_factory("a,b\n,\n,\n", "todos_nulos.csv")
        resultado = analizar_csv(ruta, eliminar_nulos=True)
        assert math.isnan(resultado["a"]["media"])
        assert math.isnan(resultado["b"]["desviacion_estandar"])

    def test_imputar_todos_nulos(self, csv_factory: Any) -> None:
        """No hay mediana para imputar si todos los valores son nulos:
        fillna con NaN → todo sigue NaN."""
        ruta = csv_factory("a,b\n,\n,\n", "todos_nulos_imputar.csv")
        resultado = analizar_csv(ruta, eliminar_nulos=False)
        assert math.isnan(resultado["a"]["media"])
        assert math.isnan(resultado["b"]["mediana"])


# =============================================================================
# Casos de error
# =============================================================================

class TestErrores:
    def test_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError, match="No se encontró"):
            analizar_csv("ruta/inexistente.csv")

    def test_columna_inexistente(self, csv_comas: str) -> None:
        with pytest.raises(ValueError, match="no existe"):
            analizar_csv(csv_comas, columnas=["no_existe"])

    def test_columna_no_numerica(self, csv_mixto: str) -> None:
        with pytest.raises(ValueError, match="no es numérica"):
            analizar_csv(csv_mixto, columnas=["nombre"])


# =============================================================================
# Mocks
# =============================================================================

class TestMocks:
    def test_mock_csv_sniffer_delimiter(self, mocker: Any, csv_comas: str) -> None:
        """Mockea csv.Sniffer para forzar un delimitador específico."""
        mock_dialect = mocker.MagicMock()
        mock_dialect.delimiter = "|"
        mock_sniffer = mocker.patch("csv.Sniffer.sniff", return_value=mock_dialect)
        # Al forzar |, pandas lee todo como una columna de texto → sin datos numéricos
        with pytest.raises(ValueError, match="No se encontraron columnas numéricas"):
            analizar_csv(csv_comas)
        assert mock_sniffer.called is True

    def test_mock_read_csv_empty(self, mocker: Any, tmp_path: Any) -> None:
        """Mockea pd.read_csv para simular EmptyDataError."""
        mocker.patch(
            "pandas.read_csv",
            side_effect=pd.errors.EmptyDataError("Simulado"),
        )
        ruta = str(tmp_path / "falso.csv")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("a,b\n1,2\n")
        with pytest.raises(pd.errors.EmptyDataError, match="Simulado"):
            analizar_csv(ruta)

    def test_mock_file_not_found_oserror(self, mocker: Any) -> None:
        """Mockea open para simular FileNotFoundError directamente."""
        mocker.patch("builtins.open", side_effect=FileNotFoundError("Simulado"))
        with pytest.raises(FileNotFoundError, match="No se encontró"):
            analizar_csv("fake.csv")

    def test_mock_sniffer_raises_empty(self, mocker: Any, tmp_path: Any) -> None:
        """Mockea Sniffer para que falle, pero la detección de vacío ocurre antes."""
        ruta = str(tmp_path / "no_vacio.csv")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("a,b\n1,2\n")
        mocker.patch("csv.Sniffer.sniff", side_effect=Exception("No importa"))
        # El Sniffer no se ejecuta si el contenido no está vacío — en realidad sí se ejecuta
        # Pero acá probamos que el error se propaga porque no hay deteccion de vacio antes
        with pytest.raises(Exception):
            analizar_csv(ruta)
