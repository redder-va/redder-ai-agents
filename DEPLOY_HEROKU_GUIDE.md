# 🚀 Deploy Backend pe Heroku (GRATIS)

## Pași Rapidi (15 minute)

### 1. Creează cont Heroku
https://signup.heroku.com/

### 2. Instalează Heroku CLI
https://devcenter.heroku.com/articles/heroku-cli

### 3. Login în terminal
```bash
heroku login
```

### 4. Creează aplicație
```bash
cd "E:\REDDER\Agenti AI"
heroku create redder-ai-backend
```

### 5. Configurează variabile environment
```bash
heroku config:set GOOGLE_API_KEY=AIzaSyA5jsAK7A3iWwXwS-YBiCgfDJpqHCu55SU
heroku config:set WC_URL=https://redder.ro
heroku config:set WC_CONSUMER_KEY=ck_91c27ab6ddbf7062eaad93982bf60d386f85688c
heroku config:set WC_CONSUMER_SECRET=cs_4cc9976d3c9973932d79a06865ddf9f611b50bb0
```

### 6. Deploy
```bash
git init
git add .
git commit -m "Initial deploy"
git push heroku main
```

### 7. URL Final
Aplicația va fi la: `https://redder-ai-backend.herokuapp.com`

### 8. Actualizează WordPress
Schimbă în plugin:
```javascript
API_URL: 'https://redder-ai-backend.herokuapp.com/chat/message'
```

## Fișiere Necesare

Trebuie să creezi în proiect:

**Procfile** (fără extensie):
```
web: gunicorn main:app
```

**runtime.txt**:
```
python-3.11.6
```

**requirements.txt** (verifică că există toate):
```
Flask==3.1.2
Flask-CORS==4.0.0
google-generativeai
woocommerce
python-dotenv
gunicorn
```

## Troubleshooting

### Eroare: "Application error"
```bash
heroku logs --tail
```

### Eroare CORS
În config.py adaugă:
```python
CORS_ORIGINS = [
    'https://redder.ro',
    'https://www.redder.ro',
    'https://redder-ai-backend.herokuapp.com'
]
```

### SSL Certificate
Heroku oferă SSL gratuit automat!
