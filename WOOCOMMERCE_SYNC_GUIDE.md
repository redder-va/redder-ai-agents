# 🔄 Sincronizare Continuă cu Redder.ro - Ghid Complet

## 📋 Prezentare Generală

Sistemul de sincronizare conectează toți agenții AI direct la magazinul online redder.ro, asigurând că toate răspunsurile, analizele și predicțiile sunt bazate strict pe date reale:

- **Produse** - Listă completă cu SKU, preț, stoc
- **Stocuri** - Status în timp real pentru fiecare produs
- **Comenzi** - Tracking comenzi și statistici vânzări
- **Categorii** - Organizare automată pe categorii

## 🎯 Agenți Conectați la Redder.ro

### ✅ Complet Integrați

1. **Inventory Manager** - Stocuri în timp real
2. **Sales Analyst** - Analize bazate pe comenzi reale
3. **Upsell Manager** - Recomandări din catalogul real
4. **Order Manager** - Tracking comenzi live
5. **Content Creator** - Descrieri pentru produse reale
6. **Marketing Agent** - Campanii bazate pe stocuri
7. **Customer Service** - Răspunsuri cu date actualizate

## 🔧 Configurare

### 1. Obține API Keys din WooCommerce

Accesează **redder.ro/wp-admin/admin.php?page=wc-settings&tab=advanced&section=keys**

Creează o cheie nouă:
- **Descriere:** "AI Agents System"
- **Permisiuni:** Read/Write
- **Consumer Key:** Salvează
- **Consumer Secret:** Salvează

### 2. Configurează .env

```bash
# WooCommerce API Credentials
WOOCOMMERCE_URL=https://redder.ro
WOOCOMMERCE_KEY=ck_your_consumer_key_here
WOOCOMMERCE_SECRET=cs_your_consumer_secret_here

# Sau folosind vechile variabile
WC_CONSUMER_KEY=ck_your_consumer_key_here
WC_CONSUMER_SECRET=cs_your_consumer_secret_here
```

### 3. Testează Conexiunea

```bash
# Activează venv
.\venv311\Scripts\activate

# Test conexiune
python test_woocommerce.py
```

Output așteptat:
```
==============================================================
TEST CONEXIUNE WOOCOMMERCE - redder.ro
==============================================================

1. Verificare conexiune...
✅ API WooCommerce conectat

2. Sincronizare produse de pe redder.ro...
✅ Sincronizat 150 produse

3. Primele 5 produse:
   1. ✅ Vodka Kumaniok Original 38% - 24.00 RON | Stoc: 45
   2. ✅ Gin Bombay Sapphire - 79.90 RON | Stoc: 23
   ...
```

## 📊 Funcționalități Serviciu WooCommerce

### Sincronizare Produse

```python
from services.woocommerce_service import get_woocommerce_service

wc = get_woocommerce_service()

# Sincronizare automată (cache 15 minute)
products = wc.sync_products()

# Forțare sincronizare
products = wc.sync_products(force=True)
```

### Căutare Produse

```python
# Căutare după nume
products = wc.search_products("vodka")

# Produs după SKU
product = wc.get_product_by_sku("VOD-001")

# Produs după ID
product = wc.get_product_by_id(1234)
```

### Status Stoc

```python
# Status stoc complet
stock = wc.get_stock_status(sku="VOD-001")
print(stock)
# {
#     "stock_quantity": 45,
#     "stock_status": "instock",
#     "in_stock": True,
#     "name": "Vodka Kumaniok",
#     "sku": "VOD-001"
# }

# Produse cu stoc scăzut
low_stock = wc.get_low_stock_products(threshold=5)

# Produse fără stoc
out_of_stock = wc.get_out_of_stock_products()
```

### Comenzi și Vânzări

```python
# Comenzi recente
orders = wc.get_recent_orders(limit=50)

# Statistici vânzări
stats = wc.get_sales_stats(days=30)
```

### Produse pe Categorii

```python
# Produse dintr-o categorie
vodka_products = wc.get_products_by_category("vodka")
rom_products = wc.get_products_by_category("rom")

# Lista categorii
categories = wc.get_categories_list()
```

## 🤖 Integrare în Agenți

### Exemplu: Inventory Manager

```python
from services.woocommerce_service import get_woocommerce_service

class InventoryManagerAgent:
    def __init__(self):
        self.wc = get_woocommerce_service()
    
    def check_stock_levels(self, item):
        # Sincronizare automată
        self.wc.sync_products()
        
        # Căutare produs
        products = self.wc.search_products(item)
        
        if not products:
            return "❌ Produs nu a fost găsit"
        
        product = products[0]
        stock = self.wc.get_stock_status(product_id=product['id'])
        
        return f"""
✅ {product['name']}
SKU: {stock['sku']}
Stoc: {stock['stock_quantity']} bucăți
Preț: {product['price']} RON
"""
```

### Exemplu: Sales Analyst

```python
class SalesAnalystAgent:
    def __init__(self):
        self.wc = get_woocommerce_service()
    
    def analyze_sales_data(self):
        # Obține comenzi reale
        orders = self.wc.get_recent_orders(limit=100)
        
        # Procesează și analizează
        total_revenue = sum(float(o['total']) for o in orders)
        
        return f"Venit total: {total_revenue:.2f} RON"
```

## ⚙️ Cache și Performanță

### Cache Automat

Sistemul folosește cache pentru a reduce numărul de request-uri:

- **Durată cache:** 15 minute (configurabil)
- **Auto-refresh:** La primul request după expirare
- **Thread-safe:** Folosește Lock pentru sincronizare

```python
# În woocommerce_service.py
self.cache_duration = timedelta(minutes=15)  # Modifică aici
```

### Verificare Cache

```python
wc = get_woocommerce_service()

# Verifică dacă trebuie refresh
if wc.needs_refresh():
    print("Cache expirat, se va actualiza")
else:
    print(f"Cache valid, ultima sincronizare: {wc.last_sync}")
```

## 📈 Monitoring și Logging

### Activare Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

Log-uri generate:
```
2026-01-09 10:30:15 - root - INFO - WooCommerce API conectat la https://redder.ro
2026-01-09 10:30:20 - root - INFO - Sincronizare produse din redder.ro...
2026-01-09 10:30:25 - root - INFO - ✅ Sincronizat 150 produse de pe redder.ro
```

## 🔄 Sincronizare Automată Periodică

### Task Scheduler (Windows)

Creează un task pentru sincronizare automată:

```powershell
# sync_products.bat
@echo off
cd /d "e:\REDDER\Agenti AI"
.\venv311\Scripts\python.exe -c "from services.woocommerce_service import get_woocommerce_service; get_woocommerce_service().sync_products(force=True)"
```

Programează în Task Scheduler:
- **Interval:** La fiecare 10 minute
- **Script:** sync_products.bat

### Cron Job (Linux)

```bash
# Sincronizare la fiecare 10 minute
*/10 * * * * cd /path/to/project && ./venv/bin/python -c "from services.woocommerce_service import get_woocommerce_service; get_woocommerce_service().sync_products(force=True)"
```

## 🆘 Troubleshooting

### Eroare: "WooCommerce API nu este conectat"

**Soluții:**
1. Verifică credentials în `.env`
2. Asigură-te că WooCommerce REST API este activat
3. Verifică permisiunile cheilor API (Read/Write)

```bash
# Test conexiune
python test_woocommerce.py
```

### Eroare: "403 Forbidden"

**Cauze:**
- API Keys incorecte
- Permisiuni insuficiente
- IP blocat de firewall

**Soluție:**
Regenerează API keys în WooCommerce cu permisiuni Read/Write

### Produse nu se sincronizează

**Verificări:**
```python
wc = get_woocommerce_service()
print(f"Conexiune: {wc.is_connected()}")
print(f"Produse în cache: {len(wc.products_cache)}")
print(f"Ultima sincronizare: {wc.last_sync}")

# Forțare sincronizare
products = wc.sync_products(force=True)
```

### Cache nu se actualizează

```python
# Resetare cache manual
wc = get_woocommerce_service()
wc.last_sync = None  # Forțează refresh
wc.products_cache = []
products = wc.sync_products(force=True)
```

## 📊 Raportare și Analytics

### Rezumat Produse

```python
wc = get_woocommerce_service()
summary = wc.get_products_summary()
print(summary)
```

Output:
```markdown
📊 **Total Produse:** 150

### Produse Disponibile:

✅ **Vodka Kumaniok Original 38%** - SKU: VOD-001 | Preț: 24 RON | Stoc: 45
✅ **Gin Bombay Sapphire** - SKU: GIN-002 | Preț: 79.90 RON | Stoc: 23
...
```

### Detalii Produs Formatate

```python
details = wc.get_product_details_formatted(sku="VOD-001")
print(details)
```

## 🚀 Best Practices

### ✅ DO

1. **Cache întotdeauna:** Folosește cache-ul implicit (15 min)
2. **Forțează sync doar când:** User face action explicit (refresh button)
3. **Verifică conexiune:** Înainte de operații critice
4. **Log erori:** Pentru debugging
5. **Folosește SKU:** Pentru identificare precisă produse

### ❌ DON'T

1. **Nu sincroniza** la fiecare request
2. **Nu ignora** cache-ul
3. **Nu expune** API keys în cod
4. **Nu face** request-uri simultane (folosește lock)
5. **Nu presupune** că produsul există (verifică None)

## 📞 Contact & Suport

Pentru probleme sau întrebări:
- Email: vasil@redder.ro
- Test: `python test_woocommerce.py`
- Logs: Verifică output-ul serviciului
