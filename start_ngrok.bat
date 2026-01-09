@echo off
echo Starting Ngrok tunnel for backend...
echo.
echo IMPORTANT: Copiaza URL-ul HTTPS care apare mai jos!
echo Apoi schimba in WordPress: API_URL: 'URL_COPIAT/chat/message'
echo.
pause

REM Porneste ngrok pe portul 5000
ngrok http 5000
