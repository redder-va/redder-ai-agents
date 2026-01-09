# Instalare Agenți AI - Ghid Rapid

## Cerințe Sistem
- Python 3.11+
- Node.js 16+
- Git

## Instalare Nouă (Laptop Nou)

### 1. Instalare Dependențe Python
```bash
# Creează environment virtual
python -m venv venv311

# Activează environment
venv311\Scripts\activate

# Instalează dependențe
pip install -r requirements.txt
```

### 2. Instalare Frontend
```bash
cd frontend
npm install
cd ..
```

### 3. Configurare Environment
Creează fișier `.env` în root cu:
```
GEMINI_API_KEY=your_key_here
WOOCOMMERCE_URL=your_url
WOOCOMMERCE_KEY=your_key
WOOCOMMERCE_SECRET=your_secret
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=your_number
```

### 4. Rulare Aplicație

#### Backend
```bash
venv311\Scripts\activate
python main.py
```

#### Frontend
```bash
cd frontend
npm start
```

Sau folosește batch files:
- `run_backend.bat` - pornește backend-ul
- `run_frontend.bat` - pornește frontend-ul
- `run_production.bat` - pornește ambele

## Verificare Instalare
Accesează:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Training Agenți
```bash
venv311\Scripts\activate
python train_agents.py
```

## Notițe
- Folderele `venv311/`, `node_modules/`, `__pycache__/` nu sunt incluse în transfer
- Acestea se regenerează automat la instalare
- Verifică și configurează API keys în `.env`
