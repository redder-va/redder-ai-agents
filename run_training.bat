@echo off
REM Script pentru rulare automată training agenți
REM Folosit de Windows Task Scheduler

echo ============================================================
echo TRAINING AUTOMAT AGENTI AI - REDDER.RO
echo ============================================================
echo.
echo Data: %date% %time%
echo.

cd /d "F:\REDDER.RO\Agenti AI"

echo Activare mediu virtual...
call venv311\Scripts\activate.bat

echo.
echo Pornire training...
echo.

python train_agents.py

echo.
echo ============================================================
echo TRAINING FINALIZAT!
echo ============================================================
echo.

REM Salvează log
echo Training executat la %date% %time% >> training_history.log

pause
