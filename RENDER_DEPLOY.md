# 🚀 Deploy pe Render.com (GRATUIT - fără card)

## Pas 1: Creează cont Render
- Mergi la: https://render.com
- Click "Get Started for Free"
- Sign up cu GitHub SAU email (redder.va@gmail.com)

## Pas 2: Conectează GitHub (OPȚIONAL dar recomandat)

SAU direct upload manual (mai jos)

## Pas 3: Deploy Backend

### Opțiunea A: Cu GitHub (RECOMANDAT)

1. Creează repo pe GitHub:
   - https://github.com/new
   - Nume: `redder-ai-backend`
   - Public sau Private (ambele merg)

2. Push cod:
```bash
git remote add origin https://github.com/USERNAME/redder-ai-backend.git
git branch -M main
git push -u origin main
```

3. În Render Dashboard:
   - Click "New +" → "Web Service"
   - Connect repository: `redder-ai-backend`
   - Settings:
     * Name: `redder-ai-backend`
     * Region: Frankfurt (Europe)
     * Branch: `main`
     * Build Command: `pip install -r requirements.txt`
     * Start Command: `gunicorn main:app`
   - Environment Variables:
     * GOOGLE_API_KEY = AIzaSyA5jsAK7A3iWwXwS-YBiCgfDJpqHCu55SU
     * WC_URL = https://redder.ro
     * WC_CONSUMER_KEY = ck_91c27ab6ddbf7062eaad93982bf60d386f85688c
     * WC_CONSUMER_SECRET = cs_4cc9976d3c9973932d79a06865ddf9f611b50bb0
     * FLASK_ENV = production
   - Instance Type: Free
   - Click "Create Web Service"

### Opțiunea B: Fără GitHub (Manual)

1. În Render Dashboard:
   - Click "New +" → "Web Service"
   - Click "Build and deploy from a Git repository"
   - SAU "Deploy an existing image"
   
2. Upload manual prin Git (vezi mai jos)

## Pas 4: Așteaptă Deploy (2-5 minute)

Vei vedea logs live. După finalizare, URL-ul va fi:
```
https://redder-ai-backend.onrender.com
```

## Pas 5: Testează

```
https://redder-ai-backend.onrender.com/health
```

Ar trebui să returneze:
```json
{"status": "healthy", "app": "Redder AI Backend"}
```

## Pas 6: Actualizează WordPress

În plugin, schimbă:
```javascript
API_URL: 'https://redder-ai-backend.onrender.com/chat/message'
```

## 🆚 Render vs Heroku

| Feature | Render | Heroku |
|---------|--------|--------|
| Cost Gratis | ✅ Fără card | ❌ Cere card |
| Build Time | ~3 min | ~2 min |
| Sleep după inactivitate | După 15 min | După 30 min |
| SSL Gratuit | ✅ | ✅ |
| Custom Domains | ✅ | ✅ |

## ⚠️ Limitări Plan Gratuit Render

- Aplicația **"adoarme"** după 15 minute de inactivitate
- Prima cerere după sleep durează ~30 secunde (cold start)
- 750 ore/lună compute time (suficient!)
- Perfect pentru teste și trafic mic-mediu

## 💡 Soluție Cold Start

Adaugă un cron job gratuit care ping-uiește aplicația la 10 minute:
- Render oferă Cron Jobs gratuite!
- Ping: `https://redder-ai-backend.onrender.com/health`

---

**NEXT:** Urmează pașii și în 5 minute chat-ul va fi LIVE! 🚀
