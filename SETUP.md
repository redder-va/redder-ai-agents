# 🚀 Setup Ghid - Instalare pe Laptop Nou

Ghid complet pentru mutarea aplicației pe un alt laptop.

---

## 📋 Prerequisite

### 1. **Python 3.11+**
```powershell
# Verifică versiunea
python --version

# Dacă nu ai Python, descarcă de la:
# https://www.python.org/downloads/
```

### 2. **Git**
```powershell
# Verifică dacă ai Git
git --version

# Dacă nu, descarcă de la:
# https://git-scm.com/download/win
```

### 3. **Node.js & npm** (pentru frontend)
```powershell
# Verifică versiunea
node --version
npm --version

# Dacă nu ai, descarcă de la:
# https://nodejs.org/
```

---

## 📥 Pas 1: Clone Repository

```powershell
# Navighează unde vrei să instalezi
cd C:\Projects  # sau orice alt folder

# Clone repository-ul
git clone https://github.com/redder-va/redder-ai-agents.git

# Intră în folder
cd redder-ai-agents
```

---

## 🔧 Pas 2: Setup Backend (Python)

### 2.1 Creează Virtual Environment
```powershell
# Creează venv
python -m venv venv311

# Activează venv
.\venv311\Scripts\activate

# Vei vedea (venv311) în prompt
```

### 2.2 Instalează Dependențe
```powershell
pip install -r requirements.txt
```

### 2.3 Configurare .env

**Copiază fișierul template:**
```powershell
copy .env.example .env
```

**Editează `.env` cu credențialele tale:**
```env
# Google AI Studio API Key
GOOGLE_API_KEY=AIza...your_key_here

# WooCommerce
WC_URL=https://redder.ro
WC_CONSUMER_KEY=ck_...
WC_CONSUMER_SECRET=cs_...

# Telegram Bot
TELEGRAM_BOT_TOKEN=1234567890:ABC...
TELEGRAM_CHAT_ID=8310296357
```

**🔑 Unde găsești credențialele:**

1. **Google AI Key**: https://aistudio.google.com/app/apikey
2. **WooCommerce Keys**: https://redder.ro/wp-admin/admin.php?page=wc-settings&tab=advanced&section=keys
3. **Telegram Bot**: https://t.me/BotFather
   - Trimite: `/newbot` (dacă creezi bot nou)
   - SAU folosește bot-ul existent: `@Redervabot`
   - Chat ID: Trimite mesaj la bot, apoi call API: `https://api.telegram.org/bot<TOKEN>/getUpdates`

---

## 🎨 Pas 3: Setup Frontend (React)

```powershell
# Navighează în folder frontend
cd frontend

# Instalează dependențe Node.js
npm install

# Întoarce-te în root
cd ..
```

---

## ✅ Pas 4: Test Local

### 4.1 Pornește Backend
```powershell
# Asigură-te că venv e activ
.\venv311\Scripts\activate

# Rulează server Flask
python main.py
```

✅ **Backend pornit pe:** http://127.0.0.1:5000

**Test endpoint:**
```powershell
# În alt terminal
curl http://127.0.0.1:5000/health
```

Răspuns așteptat:
```json
{"status": "healthy"}
```

### 4.2 Pornește Frontend (opțional)
```powershell
# În alt terminal
cd frontend
npm start
```

✅ **Dashboard pornit pe:** http://localhost:3000

---

## 🌐 Pas 5: Deploy pe Render (Producție)

Aplicația e deja configurată pentru auto-deploy:

1. **Push changes la GitHub:**
```powershell
git add .
git commit -m "Update from new laptop"
git push origin main
```

2. **Render face auto-deploy** în 2-3 minute
3. **Verifică:** https://redder-ai-backend.onrender.com/health

**Documentație completă:** [RENDER_DEPLOY.md](RENDER_DEPLOY.md)

---

## 📁 Structură Fișiere

După instalare, vei avea:

```
redder-ai-agents/
├── .env                    # Credențiale (IMPORTANT: Nu commit!)
├── .env.example            # Template pentru .env
├── main.py                 # Backend Flask
├── requirements.txt        # Dependențe Python
├── render.yaml            # Config Render deployment
├── agents/                # 15 agenți AI
├── frontend/              # React dashboard
│   ├── node_modules/     # (auto-generat de npm install)
│   └── src/
├── venv311/              # Virtual environment (auto-generat)
└── ...
```

---

## 🔍 Troubleshooting

### ❌ Eroare: "No module named 'flask'"
**Soluție:** Activează virtual environment
```powershell
.\venv311\Scripts\activate
pip install -r requirements.txt
```

### ❌ Eroare: "GOOGLE_API_KEY not found"
**Soluție:** Verifică fișierul `.env`
```powershell
# Verifică că există
dir .env

# Editează și adaugă key-ul
notepad .env
```

### ❌ Frontend: "npm: command not found"
**Soluție:** Instalează Node.js de la https://nodejs.org/

### ❌ Git: "Permission denied (publickey)"
**Soluție:** Configurează SSH key pentru GitHub
```powershell
# Generează SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Adaugă la GitHub: Settings > SSH and GPG keys
```

---

## 📝 Checklist Final

- [ ] Python 3.11+ instalat
- [ ] Git instalat
- [ ] Repository clonat: `git clone https://github.com/redder-va/redder-ai-agents.git`
- [ ] Virtual environment creat: `python -m venv venv311`
- [ ] Dependențe instalate: `pip install -r requirements.txt`
- [ ] Fișier `.env` configurat cu toate credențialele
- [ ] Frontend dependencies: `cd frontend && npm install`
- [ ] Test backend: `python main.py` → http://127.0.0.1:5000/health
- [ ] Test frontend (opțional): `npm start` → http://localhost:3000

---

## 🚀 Next Steps

După instalare:

1. **Testează agenții AI** - Accesează dashboard sau call API endpoints
2. **Verifică notificări Telegram** - Trimite test notification
3. **Personalizează** - Ajustează configurări în `config.py`
4. **Deploy** - Push la GitHub pentru auto-deploy pe Render

---

## 📚 Documentație Suplimentară

- **README.md** - Overview aplicație
- **RENDER_DEPLOY.md** - Deployment în cloud
- **GitHub Repository** - https://github.com/redder-va/redder-ai-agents

---

**Need help?** Check existing documentation or review code comments.

**Developed with ❤️ by Redder Team**
