# Conda to Poetry Converter

A simple Python script that converts conda-style `pyproject.toml` files to Poetry format.

⚠️ This whole project and README are AI-generated so watch your step.

## Installation

```bash
poetry install
```

## Usage

```bash
poetry run python converter.py --file path/to/conda_pyproject.toml > poetry_pyproject.toml
```

## Features

- Converts basic project metadata (name, version, description, authors)
- Handles dependencies with version specifiers
- Supports complex dependencies with Python version constraints
- Converts optional dependencies to Poetry extras
- Handles git and URL-based dependencies
- Maintains version specification patterns

## Example

Input (`conda_pyproject.toml`):
```toml
[project]
name = "example-package"
version = "0.1.0"
dependencies = [
    "requests>=2.28.0,<3.0.0",
    {"scipy" = {version = ">=1.9.0", python = ">=3.8"}}
]
```

Output:
```toml
[tool.poetry]
name = "example-package"
version = "0.1.0"

[tool.poetry.dependencies]
requests = ">=2.28.0,<3.0.0"
scipy = { version = ">=1.9.0", python = ">=3.8" }
``` 

## Known Issues

- May not convert the `authors` section correctly.
- May not get the python version needed
- If the conda author didn't specify versions, `poetry` may take a long
    time to resolve several dependencies with version `*`
