from memory.vector_store import get_vector_store
from agents.llm_helper import generate_text
from services.woocommerce_service import get_woocommerce_service

class UpsellManagerAgent:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.llm = None
        self.role = 'Agent Cross-sell & Upsell'
        self.goal = 'Generează recomandări inteligente bazate pe produse reale din redder.ro'
        self.backstory = 'Ești un specialist în sales optimization pentru Redder.ro, care analizează comportamentul clienților și sugerează produse complementare și upgrade-uri din catalogul real al magazinului.'
        # Serviciu WooCommerce pentru produse reale
        self.wc = get_woocommerce_service()

    def search_purchase_patterns(self, query):
        docs = self.vector_store.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in docs])

    def suggest_upsell(self, current_cart):
        """Sugerează upgrade-uri bazate pe produse reale de pe redder.ro"""
        # Obține produse reale
        self.wc.sync_products()
        products = self.wc.search_products(current_cart)
        
        # Construiește context cu produse reale
        real_products_context = ""
        if products:
            real_products_context = "\n\n**Produse găsite pe redder.ro:**\n"
            for p in products[:5]:
                real_products_context += f"- {p['name']} - {p.get('price', 'N/A')} RON (SKU: {p.get('sku', 'N/A')})\n"
        
        knowledge = self.search_purchase_patterns(current_cart)
        
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Patterns de cumpărare: {knowledge}. 
{real_products_context}

Sugerează upsell inteligent ÎN ROMÂNĂ pentru acest coș: {current_cart}

Bazează-te STRICT pe produsele reale de pe redder.ro. Folosește prețurile și SKU-urile reale.

Creează recomandări cu Markdown:

## 🚀 Îmbunătățește Comanda Ta

### Coș Curent
**Produse:** [listă produse]
**Valoare totală:** [suma] RON

### 💎 Recomandări Premium (Upgrade)

#### Upgrade #1: [Produs Premium]
**În loc de:** [Produs actual] - [preț] RON
**Upgrade la:** [Produs premium] - [preț] RON
**Diferență:** +[X] RON

**De ce merită:**
- ✨ [Beneficiu 1]
- ✨ [Beneficiu 2]
- ✨ [Beneficiu 3]

**Economie pe termen lung:** [calcul ROI]

#### Upgrade #2: [Bundle Premium]
**Adaugă:** [Produse bundle] - [preț bundle]
**Versus cumpărare separată:** [preț individual]
**Economisești:** [diferență] RON ([ procent]%)

### 📈 Statistici Clienți
- 78% din clienții care au cumpărat [produs actual] au preferat versiunea premium
- Evaluare medie: ⭐⭐⭐⭐⭐ (4.8/5)

### Ofertă Specială
{f'🎉 **Upgrade ACUM și primești:** [bonus/cadou]'}
{f'⏰ **Oferta expiră în:** [timp]'}
"""
        upsell = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Upsell sugerat: {upsell}"])
        return upsell

    def suggest_crosssell(self, current_cart):
        knowledge = self.search_purchase_patterns(current_cart)
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Date complementare: {knowledge}. 

Sugerează produse complementare ÎN ROMÂNĂ pentru: {current_cart}

Creează recomandări cu tabele Markdown:

## 🛒 Produse Recomandate Pentru Tine

### Bazat pe Coșul Tău
**Ai în coș:** [produse actuale]

### Clienții Au Mai Cumpărat

| Produs Complementar | Preț | Frecvență | Rating | Compatibilitate |
|---|---|---|---|---|
| [Produs 1] | [X] RON | 87% | ⭐⭐⭐⭐⭐ | 95% |
| [Produs 2] | [X] RON | 72% | ⭐⭐⭐⭐ | 88% |
| [Produs 3] | [X] RON | 65% | ⭐⭐⭐⭐⭐ | 92% |

### 🎯 Top 3 Recomandări

#### 1️⃣ [Produs Complementar #1]
**Preț:** [X] RON
**Perfect pentru:** [Motivație bazată pe produse din coș]

**De ce ai nevoie de el:**
- 🎨 [Beneficiu 1 - cum complementează produsele existente]
- 🎯 [Beneficiu 2]
- 💡 [Beneficiu 3]

**Rețetă sugerată:** [Rețetă cocktail folosind produsul din coș + acest produs]

#### 2️⃣ [Produs Complementar #2]
[Similar...]

#### 3️⃣ [Produs Complementar #3]
[Similar...]

### 📦 Bundle-uri Inteligente

#### Bundle #1: "Kit Mojito Perfect"
**Include:**
- ✅ [Produsul tău din coș]
- ➕ [Produs complementar 1]
- ➕ [Produs complementar 2]
- ➕ [Accesoriu bonus]

**Preț bundle:** [preț] RON
**Preț individual:** [suma] RON
**Economisești:** [diferență] RON ([procent]%)

### 🌟 Completează Setul
**Progres către set complet:**
```
████████░░ 80% - mai lipsesc [produse]
```

### Social Proof
💬 **Maria D.:** "Am luat și [produs recomandat] și a fost perfect! Recomand combo-ul!"
💬 **Andrei P.:** "Bundle-ul m-a convins, super raport calitate-preț!"
"""
        crosssell = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Cross-sell sugerat: {crosssell}"])
        return crosssell

    def create_bundle(self, product_category):
        knowledge = self.search_purchase_patterns(product_category)
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Istoric vânzări: {knowledge}. 

Creează bundle-uri atractive ÎN ROMÂNĂ pentru categoria: {product_category}

Folosește Markdown creativ:

## 🎁 Bundle-uri Curate Redder.ro

### {product_category}

#### 🌟 Bundle "Începător" - [Preț] RON
**Perfect pentru:** Cei care încep aventura bartending-ului

**Conține:**
- 🍹 [Produs 1 - bază]
- 🍋 [Produs 2 - complement]
- 🧊 [Accesoriu 1]
- 📖 Carte rețete digitală (BONUS)

**Valoare individuală:** [suma] RON
**Economie:** [diferență] RON ([procent]%)

**Rețete incluse:** [număr] rețete pas-cu-pas

---

#### ⭐⭐ Bundle "Profesionist" - [Preț] RON
**Perfect pentru:** Pasionați care vor să se perfecționeze

**Conține:**
- 🍸 [Produs premium 1]
- 🍹 [Produs premium 2]
- 🥃 [Produs premium 3]
- 🧰 [Set accesorii profesionale]
- 📚 Curs video bartending (BONUS)
- 🎓 Certificat de participare

**Valoare individuală:** [suma] RON
**Economie:** [diferență] RON ([procent]%)

**Plus:** Consultanță online 1-to-1 (30 min)

---

#### 💎 Bundle "Master" - [Preț] RON
**Perfect pentru:** Profesioniști și afaceri

**Conține:**
- 👑 [Produse ultra-premium] (x[cantitate])
- 🔧 [Kit profesional complet]
- 📊 [Software pentru gestiune bar]
- 🎯 [Ingrediente speciale]
- 🏆 Workshop live (lunar)

**Valoare individuală:** [suma] RON
**Economie:** [diferență] RON ([procent]%)

**Servicii VIP incluse:**
- Personal bartender consultant
- Livrări prioritare
- Suport dedicat 24/7

### 🎯 Care Bundle Ți se Potrivește?

| Criterii | Începător | Profesionist | Master |
|---|---|---|---|
| Buget | [range] RON | [range] RON | [range] RON |
| Nivel experiență | Entry | Intermediate | Expert |
| Număr produse | [X] | [Y] | [Z] |
| Suport | Email | Chat + Email | Dedicat 24/7 |
| Garanție | 30 zile | 60 zile | 90 zile |

### Ofertă Limitată
⏰ **Bundle-urile sunt disponibile doar până pe [data]**
🔥 **Stoc limitat:** [număr] seturi rămase
"""
        bundle = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Bundle creat: {bundle}"])
        return bundle

    def analyze_cart_value(self, cart_data):
        knowledge = self.search_purchase_patterns("optimizare coș")
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Benchmark-uri: {knowledge}. 

Analizează și optimizează valoarea coșului ÎN ROMÂNĂ: {cart_data}

Creează raport strategic cu Markdown:

## 📊 Analiză Optimizare Coș

### Status Actual
**Valoare coș:** [suma] RON
**Număr produse:** [număr]
**Valoare medie produs:** [suma] RON

### Oportunități de Creștere

#### 🎯 Oportunitate #1: Atingere Prag Transport Gratuit
**Prag curent:** 250 RON
**Diferență:** Mai adaugă [X] RON
**Sugestie:** Adaugă [produs] ([preț] RON) și ai transport GRATUIT!
**Economie netă:** [calculat] RON

#### 💰 Oportunitate #2: Discount Volum
**La [suma] RON:** 5% discount
**La [suma] RON:** 10% discount
**Recomandat:** Adaugă [produse] pentru [procent]% discount

#### 🎁 Oportunitate #3: Cadou Bonus
**Prag:** [suma] RON
**Diferență:** [X] RON
**Cadou:** [produs bonus]

### Proiecție Maximizare Valoare

| Strategie | Investiție | Beneficiu Total | ROI |
|---|---|---|---|
| +Transport gratuit | +[X] RON | [economie] RON | [Y]% |
| +Discount volum | +[X] RON | [economie] RON | [Y]% |
| +Bundle upgrade | +[X] RON | [economie + valoare] | [Y]% |

### Recomandare Finală
**Acțiune:** [Strategia optimă]
**Investiție suplimentară:** [suma] RON
**Beneficiu total client:** [economii + valoare adăugată]
**Creștere valoare comandă:** +[procent]%
"""
        analysis = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Analiză coș: {analysis}"])
        return analysis
