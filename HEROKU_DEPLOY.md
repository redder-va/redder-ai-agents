# 🚀 Deploy Backend pe Heroku - Ghid Complet

## 📋 Cerințe

- ✅ Cont Heroku (gratuit): https://signup.heroku.com
- ✅ Git instalat: https://git-scm.com/download/win
- ✅ Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

## ⚡ Deploy Rapid (5 minute)

### Opțiunea 1: Script Automat (RECOMANDAT)

```bash
# Rulează scriptul automat
deploy_heroku.bat
```

Script-ul va:
1. Verifica Git și Heroku CLI
2. Te conecta la Heroku
3. Crea aplicația
4. Seta variabilele environment
5. Face deploy automat

### Opțiunea 2: Manual (Pas cu Pas)

#### Pas 1: Instalare Tools

**Git:**
```bash
# Download și instalează de la:
https://git-scm.com/download/win

# Verifică instalarea:
git --version
```

**Heroku CLI:**
```bash
# Download și instalează de la:
https://devcenter.heroku.com/articles/heroku-cli

# Verifică instalarea:
heroku --version
```

#### Pas 2: Login Heroku

```bash
heroku login
# Se va deschide browser-ul pentru autentificare
```

#### Pas 3: Inițializare Git

```bash
cd "E:\REDDER\Agenti AI"

# Dacă nu ai git init deja:
git init
git add .
git commit -m "Deploy Redder AI Backend"
```

#### Pas 4: Creare Aplicație Heroku

```bash
# Alege un nume unic (ex: redder-ai-backend-2026)
heroku create redder-ai-backend

# SAU dacă numele e luat:
heroku create redder-ai-backend-xyz
```

#### Pas 5: Configurare Environment Variables

```bash
# API Keys și WooCommerce
heroku config:set GOOGLE_API_KEY=AIzaSyA5jsAK7A3iWwXwS-YBiCgfDJpqHCu55SU
heroku config:set WC_URL=https://redder.ro
heroku config:set WC_CONSUMER_KEY=ck_91c27ab6ddbf7062eaad93982bf60d386f85688c
heroku config:set WC_CONSUMER_SECRET=cs_4cc9976d3c9973932d79a06865ddf9f611b50bb0
heroku config:set FLASK_ENV=production

# Verifică setările:
heroku config
```

#### Pas 6: Deploy!

```bash
# Push la Heroku
git push heroku main

# SAU dacă branch-ul e master:
git push heroku master
```

**Deploy durează 2-5 minute.** Vei vedea în terminal:
```
remote: -----> Building on the Heroku-22 stack
remote: -----> Using buildpack: heroku/python
remote: -----> Python app detected
remote: -----> Installing python-3.11.6
remote: -----> Installing pip 24.0
remote: -----> Installing requirements with pip
remote: -----> Discovering process types
remote:        Procfile declares types -> web
remote: -----> Compressing...
remote: -----> Launching...
remote:        https://redder-ai-backend.herokuapp.com/ deployed to Heroku
```

## ✅ Verificare Deploy

### 1. Testează Health Endpoint

```bash
# În browser sau curl:
https://redder-ai-backend.herokuapp.com/health

# Ar trebui să returneze:
{"status": "healthy", "app": "Redder AI Backend"}
```

### 2. Testează Chat Endpoint

```bash
# PowerShell:
$body = @{
    message = "Bună! Ce vodka aveți?"
    history = @()
    session_id = "test123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://redder-ai-backend.herokuapp.com/chat/message" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### 3. Verifică Logs

```bash
# Vezi logs în timp real:
heroku logs --tail

# SAU ultimele 100 linii:
heroku logs -n 100
```

## 🔧 Actualizare WordPress

După deploy reușit, schimbă în **WordPress plugin**:

```javascript
// ÎNAINTE (local):
API_URL: 'https://127.0.0.1:5000/chat/message'

// DUPĂ (Heroku):
API_URL: 'https://redder-ai-backend.herokuapp.com/chat/message'
```

Salvează și refreshuiește site-ul (Ctrl + F5).

## 📊 Monitoring & Management

### Logs în Timp Real
```bash
heroku logs --tail -a redder-ai-backend
```

### Restart Aplicație
```bash
heroku restart -a redder-ai-backend
```

### Verifică Status
```bash
heroku ps -a redder-ai-backend
```

### Deschide în Browser
```bash
heroku open -a redder-ai-backend
```

### Configurare Custom Domain (Opțional)
```bash
# Adaugă domain propriu (ex: api.redder.ro)
heroku domains:add api.redder.ro -a redder-ai-backend

# Apoi configurează DNS:
# CNAME: api.redder.ro -> redder-ai-backend.herokuapp.com
```

## 🐛 Troubleshooting

### Eroare: "Application Error"

**Verifică logs:**
```bash
heroku logs --tail
```

**Probleme comune:**

1. **Module lipsă în requirements.txt**
```bash
# Adaugă modulul lipsă și redeploy:
echo "nume-modul==versiune" >> requirements.txt
git add requirements.txt
git commit -m "Add missing module"
git push heroku main
```

2. **Port greșit**
```python
# main.py trebuie să folosească PORT din environment:
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

3. **Timeout**
```
# În Procfile mărește timeout:
web: gunicorn main:app --timeout 120
```

### Eroare: "No web processes running"

```bash
# Scalează web dyno:
heroku ps:scale web=1 -a redder-ai-backend
```

### Eroare CORS

```bash
# Verifică CORS_ORIGINS în config.py:
heroku config:set CORS_ORIGINS=https://redder.ro,https://www.redder.ro
```

### Deploy Lent

**Normal:** Prima deploiere durează 3-5 minute  
**Dacă durează >10 minute:**
```bash
# Anulează și reîncearcă:
Ctrl+C
git push heroku main --force
```

## 📈 Update Aplicație (după modificări)

```bash
# 1. Fă modificările în cod
# 2. Commit:
git add .
git commit -m "Update: descriere modificări"

# 3. Push la Heroku:
git push heroku main

# Aplicația se va restarta automat cu noile modificări!
```

## 💰 Costuri Heroku

**Plan Gratuit (Eco Dynos - 5$/lună):**
- 1000 dyno hours/lună
- Suficient pentru un chat bot cu trafic mediu
- SSL gratuit inclus
- Custom domains suportate

**Plan Hobby (7$/lună):**
- Nu intră în sleep după 30 minute inactivitate
- Performanță mai bună
- Recomandat pentru producție

## 🎯 Next Steps După Deploy

1. ✅ Testează chat-ul pe redder.ro
2. ✅ Monitorizează logs pentru erori
3. ✅ Configurează custom domain (api.redder.ro)
4. ✅ Adaugă monitoring (Heroku Dashboard)
5. ✅ Setup backup database (dacă adaugi persistență)

## 📞 Support Heroku

- Documentație: https://devcenter.heroku.com
- Status: https://status.heroku.com
- Support: https://help.heroku.com

---

**Succes cu deploy-ul! 🚀**

Dacă întâmpini probleme, rulează `heroku logs --tail` și trimite-mi output-ul.
