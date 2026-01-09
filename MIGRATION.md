# 📦 Backup & Mutare pe Laptop Nou

Ghid rapid pentru backup și mutare aplicației Redder AI pe alt laptop.

---

## 🎯 Metoda Recomandată: GitHub (SIMPLĂ)

### Pe Laptop Vechi (Current)

**1. Asigură-te că totul e pe GitHub:**
```powershell
cd "E:\REDDER\Agenti AI"
git add .
git commit -m "Final backup before migration"
git push origin main
```

**2. Salvează doar fișierul `.env`:**
```powershell
# Copiază .env pe USB stick sau cloud
copy .env "D:\Backup\.env"
# SAU trimite pe email (securizat!)
```

✅ **Gata!** Tot codul e pe GitHub, doar `.env` trebuie salvat separat.

---

### Pe Laptop Nou

**1. Clone repository-ul:**
```powershell
# Navighează unde vrei să instalezi (ex: C:\Projects)
cd C:\Projects

# Clone de pe GitHub
git clone https://github.com/redder-va/redder-ai-agents.git
cd redder-ai-agents
```

**2. Setup automat:**
```powershell
.\setup.bat
```

**3. Copiază `.env` salvat:**
```powershell
# Copiază .env de pe USB/cloud în folderul proiectului
copy "D:\Backup\.env" .env
```

**4. Pornește aplicația:**
```powershell
.\start.bat
```

✅ **Gata!** Aplicația rulează identic ca pe laptop-ul vechi.

---

## 📁 Alternativă: Backup Manual Complet

### Ce Să Copiezi

**ESENȚIAL (IMPORTANT!):**
```
✅ .env                    - Credențiale (CRITIC!)
✅ data/                   - Training data și logs
```

**OPȚIONAL (se poate regenera):**
```
⚠️  venv311/              - Virtual environment (16GB, regenerabil)
⚠️  frontend/node_modules/- Node dependencies (500MB, regenerabil)
❌ __pycache__/           - Python cache (NU COPIA)
❌ .git/                  - Git history (NU COPIA, folosește GitHub)
```

### Backup Recomandat

**Fișiere de copiat (~5MB):**
```
redder-ai-agents/
├── .env                 ← CRITIC!
├── data/                ← Training data
├── agents/              ← Cod agenți
├── frontend/src/        ← Cod frontend
├── main.py
├── config.py
├── requirements.txt
└── ... (toate fișierele .py, .json, .md)
```

**NU copia:**
- `venv311/` - Se recrează cu `python -m venv venv311`
- `frontend/node_modules/` - Se recrează cu `npm install`
- `__pycache__/` - Cache Python, se regenerează
- `.git/` - Folosește GitHub în loc

---

## ⚡ Setup Rapid pe Laptop Nou (fără Git)

**1. Copiază folderul backup:**
```powershell
# Copiază folderul de pe USB/cloud
xcopy /E /I "D:\Backup\redder-ai-agents" "C:\Projects\redder-ai-agents"
cd "C:\Projects\redder-ai-agents"
```

**2. Rulează setup:**
```powershell
.\setup.bat
```

**3. Pornește:**
```powershell
.\start.bat
```

---

## 🔐 Securitate Fișier `.env`

**IMPORTANT:** `.env` conține credențiale sensibile!

### ✅ Metode Sigure de Transfer

**Opțiunea 1: USB Stick Criptat**
```powershell
copy .env E:\USB\.env
# Apoi șterge de pe USB după copiere pe laptop nou
```

**Opțiunea 2: Cloud Storage Privat** (Dropbox, Google Drive)
```powershell
# Încarcă în folder privat
# Descarcă pe laptop nou
# Șterge din cloud după
```

**Opțiunea 3: Recreare Manuală**
```powershell
# Pe laptop nou, editează .env manual:
notepad .env

# Completează credențialele de la:
# - Google AI Studio: https://aistudio.google.com/app/apikey
# - Telegram BotFather: https://t.me/BotFather
# - WooCommerce API: https://redder.ro/wp-admin
```

### ❌ NU Trimite `.env` Prin

- ❌ Email necriptat
- ❌ WhatsApp/Telegram (chiar dacă e privat)
- ❌ GitHub/Git (e în .gitignore automat)
- ❌ Slack/Discord

---

## 📋 Checklist Mutare Completă

### Pe Laptop Vechi
- [ ] `git push origin main` - tot codul pe GitHub
- [ ] Salvează `.env` securizat (USB/cloud privat)
- [ ] (Opțional) Backup folder `data/` dacă e important

### Pe Laptop Nou
- [ ] Instalează Python 3.11+ 
- [ ] Instalează Git (dacă folosești GitHub)
- [ ] Clone repository: `git clone https://github.com/redder-va/redder-ai-agents.git`
- [ ] Rulează setup: `.\setup.bat`
- [ ] Copiază `.env` salvat în folderul proiectului
- [ ] Test: `python main.py` → http://127.0.0.1:5000/health
- [ ] (Opțional) Frontend: `cd frontend && npm install && npm start`

---

## 🚨 Troubleshooting

### Eroare: "GOOGLE_API_KEY not found"
**Cauză:** `.env` lipsește sau incomplet  
**Soluție:**
```powershell
# Copiază .env de pe backup
copy "D:\Backup\.env" .env

# SAU recrează manual
copy .env.example .env
notepad .env  # Completează credențialele
```

### Eroare: "No module named 'flask'"
**Cauză:** Virtual environment nu e activ  
**Soluție:**
```powershell
venv311\Scripts\activate
pip install -r requirements.txt
```

### Git Clone: "Repository not found"
**Cauză:** Repository e privat  
**Soluție:**
```powershell
# Autentifică-te cu GitHub CLI
gh auth login

# SAU folosește backup manual (fără Git)
```

---

## 📞 Support

**Documentație:**
- [SETUP.md](SETUP.md) - Setup complet pas cu pas
- [README.md](README.md) - Overview aplicație
- [RENDER_DEPLOY.md](RENDER_DEPLOY.md) - Deployment cloud

**Repository GitHub:**  
https://github.com/redder-va/redder-ai-agents

---

## ✅ TL;DR - Super Quick

**Pe laptop vechi:**
```powershell
git push origin main
copy .env "D:\Backup\.env"
```

**Pe laptop nou:**
```powershell
git clone https://github.com/redder-va/redder-ai-agents.git
cd redder-ai-agents
.\setup.bat
copy "D:\Backup\.env" .env
.\start.bat
```

**Gata! 🎉**

---

**Developed with ❤️ by Redder Team**
