@echo off
echo ========================================
echo   DEPLOY BACKEND REDDER.RO PE HEROKU
echo ========================================
echo.

REM Verifică dacă Git este instalat
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [EROARE] Git nu este instalat!
    echo.
    echo Download Git de la: https://git-scm.com/download/win
    echo Apoi ruleaza din nou acest script.
    echo.
    pause
    exit /b 1
)

REM Verifică dacă Heroku CLI este instalat
heroku --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [EROARE] Heroku CLI nu este instalat!
    echo.
    echo Download Heroku CLI de la: https://devcenter.heroku.com/articles/heroku-cli
    echo Apoi ruleaza din nou acest script.
    echo.
    pause
    exit /b 1
)

echo [OK] Git si Heroku CLI sunt instalate!
echo.

REM Login Heroku
echo Pas 1: Login in Heroku (se va deschide browser-ul)
echo.
heroku login
if %errorlevel% neq 0 (
    echo [EROARE] Login Heroku esuat!
    pause
    exit /b 1
)

echo.
echo Pas 2: Initializare Git repository
echo.

REM Verifică dacă .git există deja
if exist ".git" (
    echo [INFO] Git repository deja exista.
) else (
    git init
    echo [OK] Git repository creat.
)

REM Adaugă fișiere
git add .
git commit -m "Deploy Redder AI Backend to Heroku" 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Nicio schimbare de comis.
)

echo.
echo Pas 3: Creează aplicație Heroku
echo.
set /p APP_NAME="Introdu numele aplicației (ex: redder-ai-backend): "

heroku create %APP_NAME%
if %errorlevel% neq 0 (
    echo [WARNING] Aplicatia probabil exista deja. Continuam...
)

echo.
echo Pas 4: Setare variabile environment
echo.

heroku config:set GOOGLE_API_KEY=AIzaSyA5jsAK7A3iWwXwS-YBiCgfDJpqHCu55SU -a %APP_NAME%
heroku config:set WC_URL=https://redder.ro -a %APP_NAME%
heroku config:set WC_CONSUMER_KEY=ck_91c27ab6ddbf7062eaad93982bf60d386f85688c -a %APP_NAME%
heroku config:set WC_CONSUMER_SECRET=cs_4cc9976d3c9973932d79a06865ddf9f611b50bb0 -a %APP_NAME%
heroku config:set FLASK_ENV=production -a %APP_NAME%

echo.
echo [OK] Variabile configurate!
echo.

echo Pas 5: Deploy aplicație
echo.
echo Acest pas poate dura 2-5 minute...
echo.

git push heroku main
if %errorlevel% neq 0 (
    echo [WARNING] Branch-ul 'main' nu exista. Incerc 'master'...
    git push heroku master
)

echo.
echo ========================================
echo   DEPLOY COMPLET!
echo ========================================
echo.
echo URL aplicatie: https://%APP_NAME%.herokuapp.com
echo.
echo NEXT STEPS:
echo 1. Testeaza API: https://%APP_NAME%.herokuapp.com/health
echo 2. Schimba in WordPress plugin:
echo    API_URL: 'https://%APP_NAME%.herokuapp.com/chat/message'
echo.
echo Pentru logs in timp real:
echo    heroku logs --tail -a %APP_NAME%
echo.
pause
