🌱 Mental Wellness AI (Lehsa) - Backend

[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/ci.yml)

A digital wellness platform that combines AI-powered therapy chat, mood tracking, music-based relaxation, and guided breathing exercises — designed to support mental well-being in an accessible, private, and stigma-free way.

This is the FastAPI backend for the Mental Wellness AI platform. It provides a /health endpoint and a POST /api/chat endpoint backed by a simple, safe mock agent.

💡 Vision

Mental health is often overlooked, despite affecting millions worldwide. Lehsa aims to provide instant emotional support, encourage positive daily habits, and create a safe space for self-reflection. Unlike typical health apps, this solution integrates both AI-driven guidance and interactive activities to engage the mind in a healthy, uplifting way.

✨ Core Features (MVP)

🧠 AI Chat Assistant – A conversational bot offering therapeutic-style support and positive reinforcement.

📓 Mood Journal & Tracker – Log emotions, track patterns, and reflect over time.

🎹 Music & Piano Tool – Play your own tunes or let the AI generate calming melodies.

🌬 Breathing & Relaxation Exercises – Guided techniques to reduce stress and anxiety.

🔐 Principles

Privacy First – All data handled securely with user consent.

Ethical AI – Clear disclaimers, red-flag detection, and supportive responses only.

Accessible Design – Simple, engaging, and stigma-free experience.

🚀 Roadmap

Phase 1: MVP with AI chat + mood tracking

Phase 2: Interactive music tool + breathing exercises

Phase 3: Advanced AI insights & therapist integration (optional)

Note: This project is still in early development — feedback and contributions are welcome!

## Backend Development

### Quick start
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

### Common commands
- Format: black .
- Lint (report): ruff check .
- Lint (auto-fix): ruff check . --fix
- Tests: pytest -q
- Tests with coverage (XML + HTML):
  - pytest -q --cov=. --cov-report=term-missing:skip-covered --cov-report=xml:coverage.xml --cov-report=html
  - Open htmlcov/index.html

### Pre-commit hooks
- pre-commit install
- pre-commit run --all-files

### CI badge
- Replace OWNER/REPO in the badge URL with your GitHub org/user and repository name once pushed.
