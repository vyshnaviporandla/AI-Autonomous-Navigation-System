@echo off
title AI Autonomous Navigation System
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found.
    echo Please check that the .venv folder exists.
    pause
    exit /b 1
)

echo Starting AI-Based Autonomous Navigation System...
".venv\Scripts\python.exe" -m src.simulator

if errorlevel 1 (
    echo.
    echo The simulator encountered an error.
)

pause
