@echo off
REM Launcher for PuRRgramacion - Python Visual de Bloques

if exist ".venv\Scripts\python.exe" (
    echo Iniciando PuRRgramacion con entorno virtual...
    ".venv\Scripts\python.exe" main.py
) else (
    echo Iniciando PuRRgramacion con python del sistema...
    python main.py
)
pause
