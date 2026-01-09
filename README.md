# 🤖 Sistem Multi-Agent AI - Redder.ro

Platformă completă de automatizare business pentru magazinul online de cocktail-uri și accesorii de bar, cu **12 agenți AI specializați** și **notificări WhatsApp automate** 📱

## 📚 Documentație Completă

**👉 [GHID_UTILIZARE.md](GHID_UTILIZARE.md) - Ghid complet cu exemple practice pentru fiecare agent**

**👉 [WOOCOMMERCE_SYNC_GUIDE.md](WOOCOMMERCE_SYNC_GUIDE.md) - Sincronizare continuă cu redder.ro (NOU!)**

**👉 [LIVECHAT_INTEGRATION_GUIDE.md](LIVECHAT_INTEGRATION_GUIDE.md) - Chat live pe website cu AI (NOU!)**

**👉 [LINKS_GUIDE.md](LINKS_GUIDE.md) - Linkuri automate trackabile în campanii**

**👉 [WHATSAPP_README.md](WHATSAPP_README.md) - Setup rapid notificări WhatsApp (5 minute)**

## 🚀 Start Rapid

### Backend (Flask API)
```bash
.\venv311\Scripts\activate
python main.py
```
✅ Server pornit pe: http://127.0.0.1:5000

### Frontend (React Dashboard)
```bash
run_frontend.bat
```
✅ Dashboard pornit pe: http://localhost:3000

### 📱 Notificări WhatsApp (NOU!)
```bash
# Test rapid
python test_whatsapp.py
```
✅ Mesaje automate la 0763038001 pentru comenzi noi

---

## 👥 12 Agenți AI Disponibili

### Customer Experience (5 agenți)
1. **Agent Serviciu Clienți** - Suport 24/7, răspunsuri automate
2. **Agent Live Chat Website** - Chat în timp real cu clienți, comparații produse, rețete 🍹 **(NOU!)**
3. **Agent Gestionare Recenzii** - Răspunsuri la review-uri, analiză sentiment
4. **Agent Fidelizare Clienți** - Program loialitate, puncte, recompense VIP
5. **Agent Cross-sell & Upsell** - Recomandări inteligente, bundle-uri

### Conținut & Marketing (4 agenți)
5. **Agent Creare Conținut** - Rețete cocktail-uri, descrieri produse
6. **Agent Marketing** - Campanii personalizate, strategii
7. **Agent Email Marketing** - Newsletter-e, campanii email automate
8. **Agent Social Media** - Postări Instagram/Facebook, calendare conținut

### Operațiuni & Logistică (4 agenți)
9. **Agent Gestionare Comenzi** - Procesare automată, tracking, probleme
10. **Agent Transport & Livrări** - Calcul costuri, optimizare rute, tracking AWB
11. **Agent Analiză Vânzări** - Rapoarte, predicții, insights
12. **Agent Gestionare Stoc** - Monitoring, sugestii comenzi furnizori

## ✨ Funcționalități Noi

### � LiveChat AI pe Website (NOU!)
- ✅ **Widget chat integrabil** pe redder.ro pentru conversații live cu clienții
- ✅ **Comparații produse** - "Care e diferența între Kumaniok și Valahia Gold?"
- ✅ **Rețete cocktailuri** - "Cum fac un Moscow Mule?" cu produse din magazin
- ✅ **Verificare stoc** în timp real și recomandări personalizate
- ✅ **Context persistent** - agentul își amintește conversația
- 📖 Vezi: [LIVECHAT_INTEGRATION_GUIDE.md](LIVECHAT_INTEGRATION_GUIDE.md)

### 🔗 Sincronizare Continuă cu Redder.ro
- ✅ **Conexiune permanentă** la magazinul real redder.ro
- ✅ **Sincronizare automată** produse, stocuri, SKU-uri, prețuri
- ✅ **Cache inteligent** - refresh automat la 15 minute
- ✅ **Date în timp real** pentru toți agenții AI
- ✅ **Tracking comenzi** și statistici vânzări live
- ✅ **Predicții bazate strict** pe date reale din magazin

**Test conexiune:**
```bash
python test_woocommerce.py
```

### 🔗 Linkuri Automate în Campanii
- ✅ Generare automată linkuri trackabile (UTM) în toate campaniile
- ✅ Tracking complet: sursă, mediu, campanie, acțiune
- ✅ Linkuri personalizate pentru fiecare categorie (vodka, rom, gin, etc.)
- ✅ CTA buttons cu tracking integrat
- ✅ Setare automată în Marketing, Email și Social Media agents

**Exemplu link generat:**
```
https://redder.ro/categorie-produs/vodka/?utm_source=ai-agent&utm_medium=email&utm_campaign=promotie-iarna&utm_content=shop-now
```

### �📱 Notificări WhatsApp Automate
- ✅ Mesaje instant la 0763038001 pentru comenzi noi
- ✅ Toate detaliile comenzii formatate profesional
- ✅ Integrare automată cu WooCommerce
- ✅ Setup în 5 minute cu Twilio
- 💰 Cost: ~$0.01/mesaj (~$8.50/lună pentru 1000 comenzi)

**[Configurare rapidă →](WHATSAPP_README.md)**

---

## 🛠️ Tech Stack

**Backend:**
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