# 🚀 Deploy pe Render.com (GRATUIT)

## ✅ Status: LIVE și FUNCȚIONAL

**URL Backend**: https://redder-ai-backend.onrender.com
**Chat Live**: https://redder.ro (widget în dreapta jos)

---

## 📋 Ce este configurat:

✅ **Backend Flask** cu 15 agenți AI  
✅ **Google Gemini API** (gemini-1.5-flash)  
✅ **Notificări Telegram** pentru comenzi noi  
✅ **Keepalive Cron Job** (ping la 10 min)  
✅ **CORS** permisiv pentru cross-domain  
✅ **SSL gratuit** automat  
✅ **Auto-deploy** la push GitHub  

---

## 🔧 Configurare Environment Variables în Render

**Serviciu: redder-ai-backend**

1. `GOOGLE_API_KEY` = `AIza...` (Google AI Studio)
2. `TELEGRAM_BOT_TOKEN` = `8229462081:AAFH5...`
3. `TELEGRAM_CHAT_ID` = `8310296357`
4. `WC_URL` = `https://redder.ro`
5. `WC_CONSUMER_KEY` = `ck_91c27ab...`
6. `WC_CONSUMER_SECRET` = `cs_4cc9976d...`
7. `FLASK_ENV` = `production`
8. `PYTHON_VERSION` = `3.11.6`

---

## 📱 Setup Telegram (pentru notificări comenzi)

**Creat deja:**
- Bot: @redder_orders_bot
- Token: 8229462081:AAFH5DouWp-nLq3-7IDd3UXvwNfnsvIDRf4
- Chat ID: 8310296357

**Pentru comenzi noi → mesaj pe Telegram instant!**

---

## ⚡ Optimizări Performanță

✅ Model rapid: `gemini-1.5-flash` (1-2 sec răspuns)  
✅ Prompt scurt și optimizat  
✅ Cache vector store limitat  
✅ Keepalive cron → fără cold start  

---

## 🔄 Cum să update-ezi codul

```bash
git add .
git commit -m "Your message"
git push origin main
```

Render va detecta automat și va redeploya în ~2-3 minute.

---

## 🧪 Test Endpoints

**Health check:**
```
GET https://redder-ai-backend.onrender.com/health
```

**Chat:**
```
POST https://redder-ai-backend.onrender.com/chat/message
Body: {"message": "Salut!", "session_id": "test123"}
```

---

## ⚠️ Limitări Plan Gratuit

- **750 ore/lună** compute time (suficient cu cron job)
- **512 MB RAM** (OK pentru aplicația noastră)
- **Cold start** eliminat prin cron job
- **SSL gratuit** ✅
- **Custom domain** posibil ✅

---

**Totul funcționează perfect! Chat-ul este LIVE! 🎉**
