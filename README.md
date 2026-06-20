# cálculo_estadisticas

[![CodeRabbit](https://img.shields.io/badge/CodeRabbit-Configurado-1f1f1f?logo=coderabbit)](https://github.com/dgamarra/calculo_estadisticas)

Paquete Python para leer archivos CSV, detectar automáticamente el delimitador y calcular estadísticas descriptivas sobre columnas numéricas.

## Instalación

```bash
pip install pandas numpy
```

## Uso como librería

```python
from calculo_estadisticas import analizar_csv

resultado = analizar_csv("datos.csv")
print(resultado)
# {'num': {'media': 85.91, 'mediana': 87.1, ...}, 'edad': {'media': 29.5, ...}}
```

## Uso como script

```bash
python -m calculo_estadisticas.analisis
python -m calculo_estadisticas.analisis datos.csv
```

## Procesar datos

El script `procesar_data.py` parsea archivos CSV simples con formato `nombre,num,edad`:

```python
from procesar_data import procesar_archivo

registros = procesar_archivo("datos.csv")
for r in registros:
    print(r)  # {'name': 'Ana', 'num': 85.5, 'age': 25}
```

## API

### `analizar_csv(ruta, eliminar_nulos=True, columnas=None)`

| Parámetro | Tipo | Default | Descripción |
|---|---|---|---|
| `ruta` | `str \| Path` | — | Ruta al archivo CSV |
| `eliminar_nulos` | `bool` | `True` | `True` → elimina filas con NaN; `False` → imputa con la mediana |
| `columnas` | `list[str]` | `None` | Columnas específicas a analizar (todas las numéricas si es `None`) |

**Retorna:** `dict[str, dict[str, float]]` con `media`, `mediana`, `desviacion_estandar`, `percentil_25`, `percentil_75`.

**Excepciones:**
- `FileNotFoundError` — el archivo no existe
- `pd.errors.EmptyDataError` — archivo vacío o sin datos
- `ValueError` — columna inexistente, no numérica, o sin columnas numéricas

### `procesar_archivo(ruta)` — `procesar_data.py`

| Parámetro | Tipo | Descripción |
|---|---|---|
| `ruta` | `str \| Path` | Ruta al archivo CSV (formato: `nombre,num,edad`) |

**Retorna:** `list[dict[str, Any]]` con los registros parseados.

## Tests

```bash
pip install pytest pytest-mock pytest-cov
pytest tests/ --cov=calculo_estadisticas --cov-report=term-missing
```

23 tests con cobertura del 100%.
