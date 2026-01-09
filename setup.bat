@echo off
echo ========================================
echo   REDDER AI - Setup Automat
echo   Instalare pe Laptop Nou
echo ========================================
echo.

REM Verificare Python
echo [1/5] Verificare Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [EROARE] Python nu este instalat!
    echo Descarca Python 3.11+ de la: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python gasit!
echo.

REM Verificare Git
echo [2/5] Verificare Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo [AVERTISMENT] Git nu este instalat.
    echo Poti descarca de la: https://git-scm.com/download/win
    echo.
) else (
    echo [OK] Git gasit!
    echo.
)

REM Creare Virtual Environment
echo [3/5] Creare Virtual Environment...
if exist venv311 (
    echo [SKIP] venv311 exista deja
) else (
    python -m venv venv311
    echo [OK] Virtual Environment creat!
)
echo.

REM Instalare Dependente Python
echo [4/5] Instalare dependente Python...
echo Aceasta poate dura 2-3 minute...
call venv311\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo [EROARE] Instalarea dependentelor a esuat!
    pause
    exit /b 1
)
echo [OK] Dependente instalate!
echo.

REM Setup .env
echo [5/5] Configurare .env...
if exist .env (
    echo [SKIP] .env exista deja
) else (
    copy .env.example .env
    echo [OK] .env creat din template
    echo.
    echo ====================================
    echo   IMPORTANT: Editeaza .env!
    echo ====================================
    echo Deschide .env si completeaza:
    echo - GOOGLE_API_KEY
    echo - TELEGRAM_BOT_TOKEN
    echo - TELEGRAM_CHAT_ID
    echo - WC_CONSUMER_KEY
    echo - WC_CONSUMER_SECRET
    echo.
    notepad .env
)
echo.

echo ========================================
echo   Setup Backend COMPLET!
echo ========================================
echo.
echo Urmatorii pasi:
echo 1. Verifica ca .env contine toate credentialele
echo 2. Ruleaza: venv311\Scripts\activate
echo 3. Apoi: python main.py
echo.
echo Pentru frontend (optional):
echo 1. cd frontend
echo 2. npm install
echo 3. npm start
echo.
echo Documentatie completa: SETUP.md
echo ========================================
pause
