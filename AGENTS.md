# cálculo_estadisticas — Agent guide

## Entrypoint
- `calculo_estadisticas/analisis.py` — single public function `analizar_csv`
- `calculo_estadisticas/__init__.py` re-exports it

## Commands
```bash
# run all tests with coverage
pytest tests/ --cov=calculo_estadisticas --cov-report=term-missing -v

# single test class
pytest tests/test_analisis.py::TestDelimitadores -v

# single test
pytest tests/test_analisis.py::TestErrores::test_file_not_found -v
```

## Notable
- **No pyproject.toml / setup.py** — no build system; pip install pandas numpy manually
- **Python 3.14**, pandas 3.0, numpy 2.4
- **Test deps**: pytest, pytest-mock, pytest-cov
- **23 tests, 100% coverage** target — any new code should match
- **Two modules in repo root**: `calculo_estadisticas/` (the package) and `procesar_data.py` (unrelated legacy script, not part of the package)
- **All docs in Spanish** — function names, error messages, test names, README
