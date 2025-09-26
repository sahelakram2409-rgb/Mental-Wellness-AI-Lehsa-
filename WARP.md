# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project overview
- Python FastAPI backend for an AI-powered mental wellness API.
- Single service, no build step required; served via Uvicorn with auto-reload in development.

High-level architecture
- Entry point: app.py
  - Configures logging (services/logging_service.configure_logging)
  - Loads settings from environment/.env (services/config.Settings)
  - Initializes FastAPI with title/version from settings
  - Includes routes.chat router under prefix /api
  - Exposes GET /health
- Routing: routes/chat.py
  - APIRouter exposing POST /api/chat
  - Validates non-empty message
  - Invokes agents.ai_agent.MentalWellnessAgent.generate_response(message, user_id)
  - Returns models.schemas.ChatResponse
- Agent layer: agents/ai_agent.py
  - Mocked agent returning a deterministic, safe canned response
  - Provider/model identifiers exposed on response (provider, model)
  - Extension point to integrate a real provider (e.g., OpenAI/Groq) using env-provided credentials
- Schemas: models/schemas.py
  - Pydantic v2 models for request/response:
    - ChatRequest(message: str, user_id?: str)
    - ChatResponse(reply: str, provider: str, model: str)
- Configuration: services/config.py
  - Uses python-dotenv (load_dotenv) so a local .env file is automatically loaded
  - Supported env vars:
    - APP_NAME (default: "Mental Wellness API")
    - APP_VERSION (default: "0.1.0")
    - MODEL_PROVIDER (default: "mock")
    - MODEL_NAME (default: "mock-model")
    - API_KEY (optional; not used by the mock agent)
- Logging: services/logging_service.py
  - Sets basic logging, quiets uvicorn logs
- Dev runners: run_backend.sh / run_backend.bat
  - Set PYTHONPATH to project root, respect PORT (default 8000), start uvicorn with --reload

Common commands
- Install dependencies
  - Windows (PowerShell):
    - py -m venv .venv
    - .\.venv\Scripts\Activate.ps1
    - python -m pip install -r requirements.txt
  - Unix/macOS (bash/zsh):
    - python3 -m venv .venv
    - source .venv/bin/activate
    - pip install -r requirements.txt

- Run the development server
  - Windows (PowerShell):
    - .\run_backend.bat
    - Or explicitly with a custom port: $env:PORT=8080; python -m uvicorn app:app --host 0.0.0.0 --port $env:PORT --reload
  - Unix/macOS:
    - chmod +x ./run_backend.sh (first time)
    - ./run_backend.sh
    - Or: PORT=8080 python -m uvicorn app:app --host 0.0.0.0 --port "$PORT" --reload

- Environment variables
  - Create a .env file in the repo root if needed. Example keys:
    - APP_NAME, APP_VERSION, MODEL_PROVIDER, MODEL_NAME, API_KEY
  - python-dotenv automatically loads .env on startup via load_dotenv()

- API smoke tests
  - Health check:
    - Windows (PowerShell):
      - curl http://localhost:8000/health
    - Unix/macOS:
      - curl http://localhost:8000/health
  - Chat endpoint (POST /api/chat):
    - Windows (PowerShell):
      - curl -Method POST -Uri http://localhost:8000/api/chat -ContentType 'application/json' -Body '{"message":"Hello","user_id":"u1"}'
    - Unix/macOS:
      - curl -X POST http://localhost:8000/api/chat -H 'Content-Type: application/json' -d '{"message":"Hello","user_id":"u1"}'

- Linting
  - Install dev dependencies (includes ruff, black, pytest):
    - Windows (PowerShell): python -m pip install -r requirements-dev.txt
    - Unix/macOS: pip install -r requirements-dev.txt
  - Format code:
    - black .
  - Lint (report only):
    - ruff check .
  - Lint and auto-fix:
    - ruff check . --fix

- Tests
  - Run all tests:
    - pytest -q
  - Run a single test file:
    - pytest -q tests/test_health.py
  - Filter by keyword:
    - pytest -q -k health
  - Run with coverage (XML + HTML):
    - pytest -q --cov=. --cov-report=term-missing:skip-covered --cov-report=xml:coverage.xml --cov-report=html
    - Open HTML at htmlcov/index.html (after running the above)

Git hooks (pre-commit)
- Enable hooks (after installing dev dependencies):
  - pre-commit install
- Run hooks against all files:
  - pre-commit run --all-files

Notes for agents
- Interactive API docs are available at /docs and /redoc when the server is running.
- Request flow summary: HTTP -> FastAPI (app.py) -> routes/chat.py -> agents/ai_agent.py -> models/schemas.py -> JSON response.
- To extend with a real model provider, replace MentalWellnessAgent.generate_response with calls to the chosen SDK and use settings.API_KEY appropriately.
