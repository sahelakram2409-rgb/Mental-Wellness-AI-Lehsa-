# ai-mental-wellness-backend

[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/ci.yml)

FastAPI backend for an AI-powered mental wellness API. Provides a /health endpoint and a POST /api/chat endpoint backed by a simple, safe mock agent.

Quick start
- Requirements: Python 3.11+, pip
- Install
  - Windows (PowerShell)
    - py -m venv .venv
    - .\.venv\Scripts\Activate.ps1
    - python -m pip install -r requirements-dev.txt
  - Unix/macOS
    - python3 -m venv .venv
    - source .venv/bin/activate
    - pip install -r requirements-dev.txt
- Run (dev)
  - Windows: .\run_backend.bat
  - Unix/macOS: ./run_backend.sh
  - Open: http://localhost:8000/docs

Common commands
- Format: black .
- Lint (report): ruff check .
- Lint (auto-fix): ruff check . --fix
- Tests: pytest -q
- Tests with coverage (XML + HTML):
  - pytest -q --cov=. --cov-report=term-missing:skip-covered --cov-report=xml:coverage.xml --cov-report=html
  - Open htmlcov/index.html

Pre-commit hooks
- pre-commit install
- pre-commit run --all-files

CI badge
- Replace OWNER/REPO in the badge URL with your GitHub org/user and repository name once pushed.
