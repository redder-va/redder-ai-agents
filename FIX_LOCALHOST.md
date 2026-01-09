# 🔧 Rezolvare Eroare "Conexiune Refuzată" - Localhost

## 🎯 Problema

Browser-ul refuză conexiunea la `https://localhost:3000` din cauza certificatului SSL autosemnat.

## ✅ Soluții Rapide

### Soluția 1: Acceptă Certificatul în Browser (RECOMANDAT)

#### Chrome / Edge
1. Accesează `https://localhost:3000`
2. Când apare **"Your connection is not private"** sau **"Conexiunea nu este privată"**
3. Click pe **"Advanced"** sau **"Avansat"**
4. Click pe **"Proceed to localhost (unsafe)"** sau **"Continuă către localhost (nesigur)"**
5. ✅ Gata! Frontend-ul se va încărca

#### Firefox
1. Accesează `https://localhost:3000`
2. Click pe **"Advanced"** sau **"Avansat"**
3. Click pe **"Accept the Risk and Continue"** sau **"Acceptă riscul și continuă"**
4. ✅ Gata!

### Soluția 2: Folosește HTTP (Fără SSL)

Modifică `package.json` în frontend pentru a rula fără HTTPS:

```bash
# Editează frontend/package.json
# Șterge HTTPS=true din script start
```

Apoi accesează: `http://localhost:3000`

### Soluția 3: Adaugă Certificatul în Trusted Root (PERMANENT)

#### Windows
```powershell
# Rulează ca Administrator
Import-Certificate -FilePath "e:\REDDER\Agenti AI\ssl\localhost.pem" -CertStoreLocation Cert:\LocalMachine\Root
```

#### După import:
- Restart browser
- Accesează `https://localhost:3000`
- ✅ Certificatul va fi de încredere

## 🚀 Start Rapid Aplicație

### Metodă 1: Script Automat (RECOMANDAT)

```bash
# Pornește tot (backend + frontend)
.\start_all.bat
```

Se vor deschide 2 ferestre:
- **Backend API** - `https://127.0.0.1:5000`
- **Frontend React** - `https://localhost:3000`

### Metodă 2: Manual

**Terminal 1 - Backend:**
```bash
cd e:\REDDER\Agenti AI
.\venv311\Scripts\python.exe -X utf8 main.py
```

**Terminal 2 - Frontend:**
```bash
cd e:\REDDER\Agenti AI\frontend
node "C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js" start
```

## 🔍 Verificare Servere Pornite

```powershell
netstat -ano | findstr ":5000 :3000"
```

Ar trebui să vezi:
```
TCP    127.0.0.1:5000    LISTENING
TCP    0.0.0.0:3000      LISTENING
```

## ❌ Oprire Servere

```powershell
# Oprește toate procesele Python și Node
Get-Process -Name python,node -ErrorAction SilentlyContinue | Stop-Process -Force
```

## 🆘 Troubleshooting

### "Port 3000 already in use"

```powershell
# Găsește procesul pe port 3000
netstat -ano | findstr ":3000"

# Oprește procesul (înlocuiește PID)
Stop-Process -Id <PID> -Force
```

### "Cannot find python.exe"

Verifică calea în `.bat` file sau folosește:
```bash
py -3.11 main.py
```

### Backend nu pornește

Verifică credentials în `.env`:
```bash
# Verifică fișierul .env
cat .env
```

Trebuie să existe:
- `GEMINI_API_KEY`
- `WOOCOMMERCE_KEY`
- `WOOCOMMERCE_SECRET`

## 📱 Acces de pe Alte Dispozitive (Telefon/Tabletă)

După ce accepți certificatul, poți accesa de pe orice device din rețea:

```
Frontend: https://192.168.1.137:3000
Backend:  https://192.168.1.137:5000
```

(IP-ul exact îl vezi în output-ul frontend-ului)

## ✅ Checklist Funcționare

- [ ] Backend pornit pe `https://127.0.0.1:5000`
- [ ] Frontend pornit pe `https://localhost:3000`
- [ ] Certificat SSL acceptat în browser
- [ ] Dashboard se încarcă fără erori
- [ ] Agenții răspund la comenzi

## 🎉 Success!

Acum poți folosi aplicația:
1. Deschide `https://localhost:3000` în browser
2. Acceptă certificatul (doar prima dată)
3. Testează agenții AI!
