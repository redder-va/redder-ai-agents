@echo off
REM ========================================
REM   REDDER AI - Quick Start
REM   Porneste Backend + Frontend
REM ========================================

echo Pornire aplicatie Redder AI...
echo.

REM Verificare venv
if not exist venv311\Scripts\activate.bat (
    echo [EROARE] Virtual environment nu exista!
    echo Ruleaza mai intai: setup.bat
    pause
    exit /b 1
)

REM Verificare .env
if not exist .env (
    echo [EROARE] Fisierul .env nu exista!
    echo Ruleaza mai intai: setup.bat
    pause
    exit /b 1
)

REM Porneste Backend in background
echo [1/2] Pornire Backend Flask...
start "Redder AI Backend" cmd /k "venv311\Scripts\activate && python main.py"
timeout /t 3 /nobreak >nul
echo [OK] Backend pornit pe http://127.0.0.1:5000
echo.

REM Porneste Frontend (daca exista node_modules)
if exist frontend\node_modules (
    echo [2/2] Pornire Frontend React...
    start "Redder AI Frontend" cmd /k "cd frontend && npm start"
    echo [OK] Frontend pornit pe http://localhost:3000
) else (
    echo [SKIP] Frontend dependencies lipsesc
    echo Daca vrei frontend: cd frontend ^&^& npm install ^&^& npm start
)

echo.
echo ========================================
echo   Aplicatie PORNITA!
echo ========================================
echo Backend:  http://127.0.0.1:5000/health
echo Frontend: http://localhost:3000 (daca e pornit)
echo.
echo Pentru a opri: inchide ferestrele CMD
echo ========================================
