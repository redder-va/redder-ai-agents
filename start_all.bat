@echo off
echo ============================================
echo PORNIRE BACKEND + FRONTEND - Redder.ro AI
echo ============================================
echo.

REM Pornește backend MINIMIZAT
start "Backend API" /MIN cmd /k "cd /d "%~dp0" && .\venv311\Scripts\python.exe -X utf8 main.py"

REM Așteaptă 5 secunde
timeout /t 5 /nobreak

REM Pornește frontend MINIMIZAT
start "Frontend React" /MIN cmd /k "cd /d "%~dp0frontend" && node "C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js" start"

echo.
echo ✅ Backend pornit pe: https://127.0.0.1:5000
echo ✅ Frontend pornit pe: https://localhost:3000
echo.
echo Ferestrele sunt MINIMIZATE în taskbar.
echo Pentru a le vedea, caută "Backend API" și "Frontend React" în taskbar.
echo.
echo Apasă orice tastă pentru a închide acest meniu...
pause
