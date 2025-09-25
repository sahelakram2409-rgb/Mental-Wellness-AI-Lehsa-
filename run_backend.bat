@echo off
setlocal enabledelayedexpansion
if "%PORT%"=="" set "PORT=8000"
set "PYTHONPATH=%CD%;%PYTHONPATH%"
python -m uvicorn app:app --host 0.0.0.0 --port %PORT% --reload
