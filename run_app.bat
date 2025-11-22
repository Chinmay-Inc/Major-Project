@echo off
echo Starting AI Investment Advisor...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Run the enhanced launcher
python launch.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Press any key to exit...
    pause >nul
)
