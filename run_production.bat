@echo off
REM Production Deployment Script pentru Redder.ro Chat AI

echo ========================================
echo REDDER.RO CHAT AI - PRODUCTION MODE
echo ========================================
echo.

cd /d "%~dp0"

REM Verifică venv
if not exist "venv311\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    pause
    exit /b 1
)

REM Verifică .env
if not exist ".env" (
    echo [ERROR] .env file not found!
    pause
    exit /b 1
)

REM Creează director logs dacă nu există
if not exist "logs" mkdir logs

echo [INFO] Starting production server...
echo [INFO] Server: Waitress (production WSGI)
echo [INFO] Port: 5000
echo.

REM Setează environment production
set FLASK_ENV=production
set ENVIRONMENT=production

REM Pornește cu waitress
echo [START] Running waitress-serve...
venv311\Scripts\waitress-serve.exe --host=127.0.0.1 --port=5000 --threads=4 main:app

REM Fallback la Python direct dacă waitress nu e instalat
if errorlevel 1 (
    echo [FALLBACK] Starting with Python directly...
    venv311\Scripts\python.exe main.py
)

pause
