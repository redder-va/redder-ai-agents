# 💬 Ghid Integrare LiveChat Widget pe Redder.ro

## 📋 Prezentare Generală

Widget-ul de chat AI permite clienților să comunice direct cu agenții AI pe site-ul redder.ro pentru:
- 🔍 **Comparații produse** - "Care e diferența între Kumaniok și Valahia Gold?"
- 🍹 **Rețete cocktailuri** - "Cum fac un Moscow Mule?"
- 📦 **Informații stoc** - "Aveți ORO del Sole Peach în stoc?"
- 💡 **Recomandări personalizate** - "Ce vodcă recomandați pentru cadou?"

## 🎯 Capabilități LiveChatAgent

### 1. Detectare Intent Automată
```python
Intenții suportate:
- product_comparison: Comparații între produse (vodka, gin, etc.)
- recipe_request: Rețete cocktailuri cu produse din magazin
- stock_inquiry: Verificare disponibilitate stoc
- product_recommendation: Sugestii personalizate
- general_info: Informații despre livrare, politici
```

### 2. Date Reale din WooCommerce
- Prețuri actualizate în timp real
- Status stoc (în stoc / fără stoc)
- Link-uri directe către produse
- Comparații bazate pe % alcool, preț, categorie

### 3. Răspunsuri Inteligente
- Context persistent în conversație
- Quick replies pentru întrebări frecvente
- Card-uri produse cu link "Vezi produs"
- Emoji-uri și ton prietenos

## 📦 Fișiere Componente

```
chat_widget.html        → Widget HTML standalone
agents/live_chat.py     → Agent backend cu AI
main.py                 → Endpoint /chat/message
services/woocommerce_service.py → Integrare WC
```

## 🚀 Integrare pe Site (3 pași)

### Pas 1: Adaugă widget-ul în footer WordPress

```html
<!-- În theme footer.php ÎNAINTE de </body> -->
<script>
(function() {
    var script = document.createElement('script');
    script.src = 'https://your-backend-url.com/static/chat_widget.js';
    script.async = true;
    document.body.appendChild(script);
})();
</script>
```

### Pas 2: Configurează backend URL

În `chat_widget.html` linia 186:
```javascript
const API_URL = 'https://your-backend-url.com/chat/message';
// Schimbă cu URL-ul backend-ului tău
```

### Pas 3: Deploy widget static

#### Opțiune A: Hosting pe același server
```bash
# Copiază fișierul în folder static
cp chat_widget.html /var/www/redder.ro/wp-content/themes/your-theme/chat_widget.html
```

#### Opțiune B: Hosting pe CDN
```bash
# Upload pe Cloudflare, AWS S3, etc.
# Apoi include URL-ul CDN în <script src="">
```

## 🔧 Configurare Backend

### 1. Verifică .env
```bash
# Asigură-te că există în .env:
WC_URL=https://redder.ro
WC_CONSUMER_KEY=ck_your_key_here
WC_CONSUMER_SECRET=cs_your_secret_here
GOOGLE_API_KEY=AIzaSy...
```

### 2. Pornește backend-ul
```bash
# Pornește API-ul Flask
python main.py

# SAU folosește batch-ul automat
start_all.bat
```

### 3. Testează endpoint-ul
```powershell
# Test manual cu curl
$body = @{
    message = "Ce vodka aveți?"
    history = @()
    session_id = "test123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://127.0.0.1:5000/chat/message" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body `
    -SkipCertificateCheck
```

## 📊 Structura Răspuns API

```json
{
  "success": true,
  "response": "Avem 3 tipuri de vodcă premium: Kumaniok 38%, Valahia Gold 40%...",
  "suggested_products": [
    {
      "name": "Vodca Kumaniok Original 38%",
      "price": "24 RON",
      "stock_status": "instock",
      "link": "https://redder.ro/produs/vodca-kumaniok",
      "sku": "KUM001"
    }
  ],
  "quick_replies": [
    "Comparație vodka",
    "Rețetă Moscow Mule",
    "Informații livrare"
  ]
}
```

## 🎨 Personalizare Widget

### Schimbă culorile gradient
```css
/* În chat_widget.html linia 37 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Înlocuiește cu culorile brand-ului tău */
```

### Modifică avatar-ul
```html
<!-- Linia 230 -->
<div class="chat-header-avatar">🍾</div>
<!-- Înlocuiește cu logo sau alt emoji -->
```

### Ajustează poziția
```css
/* Linia 14 */
bottom: 20px;
right: 20px;
/* Modifică pentru alte poziții (left, top) */
```

## 🧪 Testare Completă

### Test 1: Conversație simplă
```javascript
// Deschide widget-ul în browser
// Scrie: "Bună! Ce produse aveți?"
// Așteptat: Lista cu produse din stoc
```

### Test 2: Comparație
```javascript
// Scrie: "Care e diferența între Kumaniok și Valahia?"
// Așteptat: 
// - Comparație % alcool
// - Diferență preț
// - Card-uri produse cu link-uri
```

### Test 3: Rețetă
```javascript
// Scrie: "Cum fac un Moscow Mule?"
// Așteptat:
// - Rețetă completă
// - Produse necesare cu link-uri (vodka, ginger beer)
```

### Test 4: Quick Replies
```javascript
// Click pe "Recomandă vodcă"
// Așteptat: Sugestii personalizate cu prețuri și stoc
```

## 🐛 Troubleshooting

### Eroare: "WooCommerce API nu este conectat"
```bash
# Verifică .env
cat .env | grep WC_

# Verifică credențiale WooCommerce
# WP Admin → WooCommerce → Settings → Advanced → REST API
```

### Eroare: "CORS policy"
```python
# În config.py adaugă domeniul tău
CORS_ORIGINS = [
    'https://redder.ro',
    'https://www.redder.ro',
    'https://localhost:3000'
]
```

### Widget nu apare pe site
```javascript
// Verifică console browser (F12)
// Caută erori în Network tab
// Asigură-te că script-ul se încarcă corect
```

### Răspunsuri lente
```python
# În services/woocommerce_service.py
# Ajustează cache duration
self.cache_duration = timedelta(minutes=30)  # Mai mult cache
```

## 📈 Monitoring & Analytics

### Logs conversații
```python
# Logs salvate automat în console Flask
# Pentru salvare permanentă:
@app.route('/chat/message', methods=['POST'])
def chat_message():
    # Salvează în database
    ChatLog.create(
        session_id=data['session_id'],
        message=data['message'],
        response=result['response']
    )
```

### Metrici importante
- **Conversații/zi**: Număr de sesiuni unice
- **Intent-uri**: Ce tip de întrebări predomină
- **Produse menționate**: Care produse generează cele mai multe conversații
- **Conversii**: Click-uri pe link-uri produse → comenzi

## 🔒 Securitate

### Rate Limiting
```python
# main.py are deja rate limiting
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["200 per day", "50 per hour"])
```

### Sanitize Input
```python
# LiveChatAgent validează input-ul automat
# Pentru protecție extra:
import bleach
user_message = bleach.clean(user_message)
```

### HTTPS Obligatoriu
```bash
# Backend TREBUIE să ruleze pe HTTPS
# Chat widget folosește fetch() care necesită HTTPS pentru cross-origin
```

## 🚀 Next Steps

1. **Deploy backend pe server production**
   - Recomand: DigitalOcean, AWS, sau Heroku
   - Configurează SSL certificate (Let's Encrypt)

2. **Integrează analytics**
   - Google Analytics Events pentru click-uri
   - Track conversii chat → comandă

3. **Adaugă funcționalități**
   - Upload imagini pentru identificare produse
   - Voice input pentru comenzi vocale
   - Notificări pentru oferte personalizate

4. **A/B Testing**
   - Testează diferite formulări quick replies
   - Optimizează tonul conversațiilor
   - Măsoară impact pe conversii

## 📞 Support

Pentru probleme tehnice:
- 📧 Email: suport@redder.ro
- 💬 Chat: Direct pe redder.ro
- 📝 Docs: [WOOCOMMERCE_SYNC_GUIDE.md](WOOCOMMERCE_SYNC_GUIDE.md)

---

**Versiune**: 1.0  
**Data**: 2024  
**Autor**: Redder AI Team 🤖
