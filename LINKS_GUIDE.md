# 🔗 Linkuri Automate în Campanii - Ghid Complet

## 📋 Prezentare Generală

Sistemul de linkuri automate generează URL-uri trackabile (cu parametri UTM) pentru toate campaniile create de agenții AI. Acest lucru permite:

- **Tracking complet** al surselor de trafic și conversii
- **Măsurare ROI** pentru fiecare campanie
- **Optimizare automată** a canalelor de marketing
- **Zero configurare manuală** - linkurile se adaugă automat

## 🎯 Agenți cu Linkuri Automate

### 1. Marketing Agent
**Endpoint:** `/create/campaign`

**Exemple campanii:**
- Promoție Vodka Premium
- Black Friday Cocktail-uri
- Lansare Produs Nou

**Linkuri generate:**
```
https://redder.ro/categorie-produs/vodka/?utm_source=ai-agent&utm_medium=marketing&utm_campaign=promotie-vodka-premium&utm_content=discover
```

### 2. Email Marketing Agent
**Endpoints:** 
- `/email/campaign` - Campanii email
- `/email/newsletter` - Newsletter-e

**Linkuri generate:**
```
https://redder.ro/magazin/?utm_source=ai-agent&utm_medium=email&utm_campaign=black-friday-cocktail&utm_content=shop-now
```

### 3. Social Media Agent
**Endpoints:**
- `/social/post` - Postări social media
- `/social/calendar` - Calendar conținut

**Linkuri generate:**
```
https://redder.ro/categorie-produs/gin/?utm_source=ai-agent&utm_medium=social&utm_campaign=postare-instagram-gin&utm_content=discover
```

## 📊 Structura Parametrilor UTM

Fiecare link conține parametri pentru tracking complet:

| Parametru | Valoare | Descriere |
|-----------|---------|-----------|
| `utm_source` | `ai-agent` | Sursa traficului (fix pentru toate campaniile AI) |
| `utm_medium` | `email`, `social`, `marketing`, `newsletter` | Canalul de marketing |
| `utm_campaign` | Nume campanie (slug) | Identificator unic campanie |
| `utm_content` | `shop-now`, `discover`, `view-offer` | Tipul de acțiune |

## 🛠️ Cum Funcționează

### 1. Agent creează campanie
```python
from agents.marketing import MarketingAgent

agent = MarketingAgent()
campaign = agent.create_campaign("Promoție Vodka Premium")
```

### 2. Sistem generează linkuri automat
```python
# În background, agentul:
link_gen = get_link_generator()
campaign = link_gen.inject_links_in_campaign(campaign, "promotie-vodka", "marketing")
```

### 3. Campanie returnată cu linkuri
```markdown
## Promoție Vodka Premium

Descoperă cele mai fine vodka premium...

---

### 🔗 Linkuri Rapide:

- [🍸 Vodka](https://redder.ro/categorie-produs/vodka/?utm_source=ai-agent&utm_medium=marketing&utm_campaign=promotie-vodka&utm_content=discover)
- [🥃 Rom](https://redder.ro/categorie-produs/rom/?utm_source=ai-agent&utm_medium=marketing&utm_campaign=promotie-vodka&utm_content=discover)
- [🍹 Gin](https://redder.ro/categorie-produs/gin/?utm_source=ai-agent&utm_medium=marketing&utm_campaign=promotie-vodka&utm_content=discover)

[🛒 Cumpără Acum](https://redder.ro/magazin/?utm_source=ai-agent&utm_medium=marketing&utm_campaign=promotie-vodka&utm_content=shop-now)
```

## 📦 Categorii Suportate

Sistemul recunoaște automat categorii din textul campaniei:

| Categorie | URL Path |
|-----------|----------|
| Vodka | `/categorie-produs/vodka/` |
| Rom | `/categorie-produs/rom/` |
| Gin | `/categorie-produs/gin/` |
| Whisky | `/categorie-produs/whisky/` |
| Tequila | `/categorie-produs/tequila/` |
| Cocktail | `/categorie-produs/cocktailuri/` |
| Lichior | `/categorie-produs/lichioruri/` |
| Vin | `/categorie-produs/vinuri/` |
| Șampanie | `/categorie-produs/sampanii/` |
| General | `/magazin/` |

## 🎨 Personalizare Link Generator

### Modificare domeniu
```python
# În agents/link_generator.py
self.base_url = "https://redder.ro"  # Schimbă aici
```

### Adăugare categorii noi
```python
self.product_categories = {
    "vodka": "/categorie-produs/vodka/",
    "categoria-noua": "/path-nou/",  # Adaugă aici
}
```

### Adăugare acțiuni noi
```python
self.campaign_actions = {
    "cumpara": "shop-now",
    "actiune-noua": "action-slug",  # Adaugă aici
}
```

## 📈 Tracking în Google Analytics

Pentru a urmări performanța campaniilor:

1. **Google Analytics 4:** Mergi la **Reports > Acquisition > Traffic acquisition**
2. **Filtrează:** `Session medium` = `ai-agent`
3. **Vizualizează:** Conversii pe campanie, canal, acțiune

### Metrici Cheie
- **Sessions** - Vizite generate de campanie
- **Conversions** - Comenzi finalizate
- **Revenue** - Venituri generate
- **Conversion Rate** - Rata de conversie

## 🧪 Testare

### Test Local
```bash
# Activează venv
.\venv311\Scripts\activate

# Rulează test
python test_link_generator.py
```

### Test Agenți
```bash
python test_agents_with_links.py
```

### Test API
```bash
# Test campanie marketing
curl -X POST http://localhost:5000/create/campaign \
  -H "Content-Type: application/json" \
  -d '{"text":"Promoție Vodka Premium"}'

# Test campanie email
curl -X POST http://localhost:5000/email/campaign \
  -H "Content-Type: application/json" \
  -d '{"text":"Black Friday Cocktail-uri"}'
```

## 💡 Exemple de Utilizare

### Email Marketing
```python
from agents.email_marketing import EmailMarketingAgent

agent = EmailMarketingAgent()
campaign = agent.create_email_campaign("Valentine's Day Cocktails")
# Returnează email cu linkuri trackabile automate
```

### Social Media
```python
from agents.social_media import SocialMediaAgent

agent = SocialMediaAgent()
post = agent.create_post("Instagram - Rețete Gin Tonic")
# Returnează post cu link în bio trackabil
```

### Marketing General
```python
from agents.marketing import MarketingAgent

agent = MarketingAgent()
campaign = agent.create_campaign("Campanie Crăciun 2025")
# Returnează campanie completă cu toate linkurile
```

## 🔧 API pentru Linkuri Custom

Dacă vrei să generezi linkuri manual:

```python
from agents.link_generator import get_link_generator

link_gen = get_link_generator()

# Link simplu
link = link_gen.generate_campaign_link(
    category="vodka",
    campaign_name="promotie-iarna",
    medium="email",
    action="cumpara"
)
# https://redder.ro/categorie-produs/vodka/?utm_source=ai-agent&utm_medium=email&utm_campaign=promotie-iarna&utm_content=shop-now

# CTA Button
button = link_gen.get_cta_button(
    text="🛒 Comandă Acum",
    category="gin",
    campaign_name="flash-sale",
    medium="social"
)
# [🛒 Comandă Acum](https://redder.ro/...)

# Linkuri toate categoriile
links_md = link_gen.get_category_links_markdown("campanie-test", "email")
# Returnează Markdown cu toate categoriile
```

## 📝 Best Practices

### ✅ DO
- Folosește nume descriptive pentru campanii
- Păstrează numele campaniei scurt (max 30 caractere)
- Verifică linkurile în Google Analytics
- Monitorizează conversiile pe campanie

### ❌ DON'T
- Nu folosi spații în numele campaniei (vor fi înlocuite cu `-`)
- Nu modifica manual parametrii UTM
- Nu șterge linkurile din răspunsuri

## 🚀 Dezvoltări Viitoare

- [ ] Integrare cu Google Tag Manager
- [ ] Shortlinks (redder.ro/r/xyz)
- [ ] QR codes pentru campanii offline
- [ ] A/B testing linkuri
- [ ] Raportare automată performanță

## 🆘 Troubleshooting

### Linkurile nu apar în campanii
```bash
# Verifică că link_generator este importat
grep "from agents.link_generator" agents/*.py
```

### Linkurile nu trackează în GA4
- Verifică că site-ul are Google Analytics instalat
- Așteaptă 24-48h pentru date
- Verifică filtrele în GA4

### Eroare la generare linkuri
```bash
# Verifică sintaxa
python test_link_generator.py
```

## 📞 Contact & Suport

Pentru probleme sau întrebări:
- Email: vasil@redder.ro
- GitHub Issues: [github.com/redder/ai-agents/issues](https://github.com)
