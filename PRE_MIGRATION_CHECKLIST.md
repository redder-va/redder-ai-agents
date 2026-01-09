# ✅ Checklist Pre-Mutare Laptop

Verifică că totul e pregătit înainte de mutare.

---

## 📋 Verificare Repository GitHub

**Status GitHub:**
```powershell
cd "E:\REDDER\Agenti AI"
git status
```

✅ Trebuie să vezi: `nothing to commit, working tree clean`

**Ultimul push:**
```powershell
git log -1
```

✅ Verifică că ultimul commit e recent

**Repository URL:**
```powershell
git remote -v
```

✅ Trebuie să vezi: `https://github.com/redder-va/redder-ai-agents.git`

---

## 🔐 Verificare Credențiale (.env)

**Verifică că `.env` există:**
```powershell
dir .env
```

**Verifică conținutul:**
```powershell
type .env
```

✅ Trebuie să conțină:
- `GOOGLE_API_KEY=AIza...`
- `TELEGRAM_BOT_TOKEN=...`
- `TELEGRAM_CHAT_ID=...`
- `WC_CONSUMER_KEY=ck_...`
- `WC_CONSUMER_SECRET=cs_...`
- `WC_URL=https://redder.ro`

**Backup `.env`:**
```powershell
# Copiază pe USB/cloud
copy .env "D:\Backup\.env"
```

✅ Verifică că fișierul a fost copiat

---

## 📦 Verificare Fișiere Critice

**Fișiere esențiale care TREBUIE să existe în repository:**

```powershell
# Verifică fișierele principale
dir main.py, requirements.txt, render.yaml, README.md, SETUP.md
```

✅ Toate trebuie să existe

**Foldere critice:**
```powershell
dir agents, frontend, notifications, services
```

✅ Toate folderele trebuie să existe

---

## 🚀 Test Aplicație Locală

**1. Backend funcționează:**
```powershell
# Activează venv
.\venv311\Scripts\activate

# Pornește backend
python main.py
```

✅ Mesaj: `Running on http://127.0.0.1:5000`

**2. Test health endpoint:**
```powershell
# În alt terminal
curl http://127.0.0.1:5000/health
```

✅ Răspuns: `{"status": "healthy"}`

**3. Test agent chat:**
```powershell
curl -X POST http://127.0.0.1:5000/chat/message -H "Content-Type: application/json" -d "{\"message\":\"test\"}"
```

✅ Primești răspuns JSON de la agent

---

## ☁️ Verificare Deployment Production

**Backend Render:**
```powershell
curl https://redder-ai-backend.onrender.com/health
```

✅ Status: `healthy`

**Chat widget pe site:**
- Deschide: https://redder.ro
- Verifică widget-ul chat în dreapta jos
- Trimite un mesaj test

✅ Răspuns în 1-2 secunde

---

## 📄 Verificare Documentație

**Fișiere ghid create:**

```powershell
dir README.md, SETUP.md, MIGRATION.md, RENDER_DEPLOY.md
```

✅ Toate ghidurile există și sunt actualizate

**Scripturi setup:**
```powershell
dir setup.bat, start.bat
```

✅ Scripturile de instalare există

---

## 🎯 Checklist Final

### Repository & GitHub
- [ ] `git status` → clean working tree
- [ ] `git push origin main` → totul pe GitHub
- [ ] Repository public/privat verificat pe https://github.com/redder-va/redder-ai-agents

### Credențiale & Backup
- [ ] Fișier `.env` există local
- [ ] `.env` copiat pe USB/cloud securizat
- [ ] Toate credențialele verificate (Google, Telegram, WooCommerce)
- [ ] `.env.example` actualizat în repository

### Aplicație Funcțională
- [ ] Backend local rulează: `python main.py` → OK
- [ ] Health endpoint: http://127.0.0.1:5000/health → healthy
- [ ] Test chat agent → răspunde corect
- [ ] Production Render → https://redder-ai-backend.onrender.com/health → OK
- [ ] Chat widget pe redder.ro → funcțional

### Documentație
- [ ] README.md - actualizat cu instrucțiuni setup
- [ ] SETUP.md - ghid complet instalare
- [ ] MIGRATION.md - ghid mutare laptop
- [ ] RENDER_DEPLOY.md - documentație cloud
- [ ] setup.bat - script instalare automată
- [ ] start.bat - script pornire rapidă

### Data & Training
- [ ] Folder `data/` există cu fișiere training
- [ ] (Opțional) Backup folder `data/` pe USB

---

## 🎉 Pregătit pentru Mutare!

Dacă toate bifele sunt marcate, aplicația e pregătită 100% pentru transfer!

**Pe laptop nou vei face:**

1. Clone repository:
   ```powershell
   git clone https://github.com/redder-va/redder-ai-agents.git
   cd redder-ai-agents
   ```

2. Setup automat:
   ```powershell
   .\setup.bat
   ```

3. Copiază `.env`:
   ```powershell
   copy "D:\Backup\.env" .env
   ```

4. Pornește:
   ```powershell
   .\start.bat
   ```

**Gata în 5 minute!** 🚀

---

**Developed with ❤️ by Redder Team**
