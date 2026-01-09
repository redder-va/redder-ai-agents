# 🤖 Redder AI - Multi-Agent System

Sistem AI cu 15 agenți specializați pentru automatizarea business-ului magazinului online redder.ro.

## ✅ Status: LIVE în producție

- **Backend**: https://redder-ai-backend.onrender.com
- **Chat Live**: https://redder.ro (widget în dreapta jos)
- **Platform**: Render.com (cloud hosting gratuit)

---

## 🎯 Funcționalități

### 💬 **Chat AI Live**
- Widget interactiv pe site
- Răspunsuri instant (1-2 sec)
- Sugestii de produse personalizate
- Rețete cocktail-uri
- Model: Google Gemini 1.5 Flash

### 📱 **Notificări Telegram**
- Comenzi noi → mesaj instant pe Telegram
- Detalii complete: client, produse, total, adresă
- Bot: @Redervabot

### 🤖 **15 Agenți AI Specializați**
1. Customer Service - suport clienți 24/7
2. Content Creator - descrieri produse, rețete
3. Sales Analyst - analiză vânzări
4. Marketing - campanii personalizate
5. Inventory Manager - gestiune stoc
6. Email Marketing - newsletter automat
7. Social Media - posturi automate
8. Review Manager - răspuns la review-uri
9. Order Manager - procesare comenzi
10. Shipping Manager - logistică
11. Loyalty Manager - program fidelitate
12. Upsell Manager - recomandări cross-sell
13. Live Chat - conversații în timp real
14. Link Generator - link-uri trackabile
15. Product Scraper - importare produse

---

## 🛠️ Tehnologii

**Backend:**
- Python 3.11
- Flask + Gunicorn
- Google Gemini AI
- LangChain
- FAISS (vector store)

**Frontend:**
- React.js
- JavaScript widget

**Deployment:**
- Render.com (cloud hosting)
- GitHub auto-deploy
- Cron job keepalive

**Integrări:**
- WooCommerce API
- Telegram Bot API
- Google AI Studio

---

## 📂 Structură Proiect

```
├── agents/              # 15 agenți AI specializați
├── feedback/            # Sistem feedback și învățare
├── memory/              # Vector store (FAISS)
├── notifications/       # Telegram notifier
├── services/            # WooCommerce integration
├── frontend/            # React dashboard
├── static/              # Chat widget JS
├── main.py             # Backend API Flask
├── requirements.txt    # Dependențe Python
└── render.yaml         # Configurare Render deployment
```

---

## 🚀 Deploy

Aplicația rulează 24/7 în cloud pe Render.com. 

**Pentru update-uri:**
```bash
git add .
git commit -m "Your changes"
git push origin main
```
→ Render face auto-deploy în 2-3 minute.

**Documentație deployment:** [RENDER_DEPLOY.md](RENDER_DEPLOY.md)

---

## 🔧 Configurare Locală (Dezvoltare)

**1. Clone repository:**
```bash
git clone https://github.com/redder-va/redder-ai-agents.git
cd redder-ai-agents
```

**2. Instalează dependențe:**
```bash
python -m venv venv311
venv311\Scripts\activate
pip install -r requirements.txt
```

**3. Configurează .env:**
```
GOOGLE_API_KEY=your_key
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
WC_URL=https://redder.ro
WC_CONSUMER_KEY=your_key
WC_CONSUMER_SECRET=your_secret
```

**4. Rulează:**
```bash
python main.py
```

---

## 📊 Limitări Plan Gratuit Render

- 750 ore/lună (suficient cu keepalive cron)
- 512 MB RAM
- Cold start eliminat prin ping automat
- SSL gratuit inclus

---

## 📝 Licență

Proprietary - Redder.ro © 2026

---

**Developed with ❤️ by Redder Team**
- Python 3.11.6 (venv311)
- Flask 3.1.2 + Flask-CORS
- Google Gemini API (gemini-2.0-flash)
- LangChain + FAISS Vector Store
- WooCommerce API Integration
- PyTorch + Sentence Transformers

**Frontend:**
- React 18.2.0
- ReactMarkdown + remark-gfm
- Axios pentru API calls
- CSS custom (Word-like formatting)

## ✨ Caracteristici Principale

✅ **Formatare Markdown** - Toate răspunsurile cu titluri, liste, tabele
✅ **Limba Română** - Interfață și conversații 100% în română
✅ **Lazy Loading** - Agenții se încarcă doar când sunt folosiți
✅ **Memorie Vectorială** - Învață din interacțiuni
✅ **Integrare WooCommerce** - Date reale comenzi/stoc
✅ **24/7 Disponibilitate** - Răspunsuri instant
✅ **🆕 Antrenare Automată** - Agenții învață despre produsele de pe site

---

## 🎓 Antrenare Automată Agenți

**👉 [TRAINING_GUIDE.md](TRAINING_GUIDE.md) - Ghid complet antrenare automată**

### Quick Start Training:
```bash
# Activează mediul virtual
.\venv311\Scripts\activate

# Antrenează agenții cu produsele de pe Redder.ro
python train_agents.py
```

**Ce face:**
- Extrage toate produsele de pe site (WooCommerce API)
- Procesează descrieri, prețuri, stocuri, categorii
- Antrenează agenții să răspundă cu informații reale
- Agenții vor cunoaște: disponibilitate, prețuri, caracteristici

**Beneficii:**
- Răspunsuri precise despre produse reale
- Actualizare automată cunoștințe
- Training zilnic programabil
- Zero intervenție manuală
- Memory: ChromaDB
- Feedback: SQLite