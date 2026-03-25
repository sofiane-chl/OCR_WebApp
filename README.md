# OCR WebApp

A modular, production-ready OCR web application built with **FastAPI** + **pytesseract**, managed with **Poetry**.

## Features

- REST API for image-to-text extraction
- Pluggable architecture — extend without touching core logic
- Structured logging, typed configuration (pydantic-settings)
- Full test suite (pytest + coverage)
- Lint/format pipeline (ruff + black + mypy)
- GitHub Actions CI out of the box

---

## Quick Start

### Prerequisites

- Python ≥ 3.11
- [Poetry](https://python-poetry.org/docs/#installation)
- Tesseract OCR engine — `sudo apt install tesseract-ocr` (Ubuntu) or `brew install tesseract` (macOS)

### Install

```bash
# Clone the repo
git clone <your-repo-url> && cd OCR_WebApp

# Install dependencies (including dev tools)
poetry install --with dev

# Copy and configure environment variables
cp .env.example .env
```

### Run

```bash
poetry run uvicorn ocr_webapp.api.app:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API docs.

---

## Project Structure

```
OCR_WebApp/
├── ocr_webapp/
│   ├── core/          # OCR engine and processing pipeline
│   ├── api/           # FastAPI routes and app factory
│   ├── models/        # Pydantic schemas
│   ├── services/      # External integrations (DB, storage, etc.)
│   ├── plugins/       # Drop-in plugin system
│   └── utils/         # Config, logging, shared helpers
├── tests/
│   ├── unit/          # Fast, isolated unit tests
│   └── integration/   # Tests that exercise the full stack
├── scripts/           # One-off dev/ops scripts
├── docs/              # Project documentation
└── .github/workflows/ # GitHub Actions CI
```

---

## Development

```bash
# Run tests with coverage
poetry run pytest

# Lint
poetry run ruff check .

# Format
poetry run black .

# Type check
poetry run mypy ocr_webapp/
```

---

## Adding a Plugin

```python
from ocr_webapp.plugins.base import BasePlugin, PluginRegistry

class MyPlugin(BasePlugin):
    name = "my_plugin"

    def process(self, text: str, **kwargs) -> str:
        # transform text here
        return text.lower()

PluginRegistry.register(MyPlugin())
```

---

## Configuration

All settings are loaded from environment variables (or `.env`). See [`.env.example`](.env.example) for the full list.

| Variable              | Default        | Description                  |
|-----------------------|----------------|------------------------------|
| `DEBUG`               | `false`        | Enable debug mode            |
| `LOG_LEVEL`           | `INFO`         | Logging verbosity            |
| `TESSERACT_LANG`      | `eng`          | Tesseract language code      |
| `MAX_UPLOAD_SIZE_MB`  | `10`           | Max image upload size in MB  |

---

## License

MIT
