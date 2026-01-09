from memory.vector_store import get_vector_store
from agents.llm_helper import generate_text

class ShippingManagerAgent:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.llm = None
        self.role = 'Agent Transport & Livrări'
        self.goal = 'Optimizează logistica, calculează costuri transport și urmărește livrări'
        self.backstory = 'Ești un specialist în logistică pentru Redder.ro, care optimizează rutele de livrare, negociază cu curierii, calculează costuri și asigură livrări la timp.'

    def search_shipping_data(self, query):
        docs = self.vector_store.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in docs])

    def calculate_shipping(self, order_details):
        knowledge = self.search_shipping_data(order_details)
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Date transport: {knowledge}. 

Calculează costul și opțiunile de transport ÎN ROMÂNĂ pentru: {order_details}

Folosește tabele Markdown:

## 📦 Opțiuni Transport

### Detalii Comandă
**Destinație:** [oraș, județ]
**Greutate estimată:** [X] kg
**Valoare comandă:** [suma] RON

### Opțiuni Disponibile

| Curier | Timp Livrare | Cost | Asigurare | Tracking | Recomandat |
|---|---|---|---|---|---|
| Fan Courier | 1-2 zile | [X] RON | Inclusă | ✅ | ⭐⭐⭐ |
| DPD | 1-3 zile | [X] RON | Opțional | ✅ | ⭐⭐ |
| Cargus | 2-4 zile | [X] RON | Inclusă | ✅ | ⭐ |
| Curier Rapid | 1 zi | [X] RON | Inclusă | ✅ | ⭐⭐⭐ (express) |
| Ridicare personală | 0 zile | 0 RON | - | - | ⭐⭐ |

### Recomandare
**Opțiunea recomandată:** [Curier] - [motivație]

### Transport Gratuit
{f'✅ **Comanda calificată pentru transport gratuit!** (peste [suma] RON)' if '[valoare_comanda]' > '200' else f'❌ Mai adaugă [diferența] RON pentru transport gratuit'}

### Zona Livrare
**Tip zonă:** [Urban/Rural/Izolat]
**Surcharge special:** [DA/NU] - [detalii]
"""
        shipping = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Calcul transport: {shipping}"])
        return shipping

    def optimize_routes(self, delivery_list):
        knowledge = self.search_shipping_data("optimizare rute")
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Experiență rute: {knowledge}. 

Optimizează rutele de livrare ÎN ROMÂNĂ pentru aceste comenzi: {delivery_list}

Creează plan cu Markdown:

## 🗺️ Plan Optimizare Rute Livrare

### Comenzi de Procesat
**Total comenzi:** [număr]
**Orașe destinație:** [listă orașe]
**Data livrare țintă:** [data]

### Rute Optimizate

#### 📍 Ruta 1: [Nume Rută]
**Orașe:** [oraș1] → [oraș2] → [oraș3]
**Distanță totală:** [X] km
**Timp estimat:** [X] ore
**Comenzi:** #[id1], #[id2], #[id3]

| Stop | Oraș | Adresă | Comandă | Timp Estimat | Prioritate |
|---|---|---|---|---|---|
| 1 | [oraș] | [adresă] | #[id] | 09:00-10:00 | 🔴 Urgentă |
| 2 | [oraș] | [adresă] | #[id] | 10:30-11:00 | 🟡 Medie |
| 3 | [oraș] | [adresă] | #[id] | 11:30-12:00 | 🟢 Normală |

#### 📍 Ruta 2: [Nume Rută]
[Similar...]

### Economii
**Distanță economisită:** [X] km vs rute neoptimizate
**Timp economisit:** [X] ore
**Cost redus:** [X] RON

### Instrucțiuni Șofer
- [Instrucțiune 1]
- [Instrucțiune 2]
"""
        routes = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Rute optimizate: {routes}"])
        return routes

    def track_delivery(self, tracking_number):
        knowledge = self.search_shipping_data(f"tracking {tracking_number}")
        prompt = f"""Tu ești {self.role}. {self.backstory}. 

Generează status livrare ÎN ROMÂNĂ pentru AWB: {tracking_number}

Folosește emoji și timeline Markdown:

## 📍 Tracking Livrare AWB: {tracking_number}

### Status Curent
**Poziție:** [Locație]
**Status:** [În tranzit/La depozit/În livrare/Livrată]
**Ultima actualizare:** [data și ora]

### Istoric Livrare
```
🟢 [Data] [Ora] - Colet preluat de la expeditor (București)
🟢 [Data] [Ora] - Sosit în depozit sortare (București)
🔵 [Data] [Ora] - În tranzit către [oraș destinație]
🟡 [Data] [Ora] - Sosit în depozit local ([oraș])
🟠 [Data] [Ora] - În curs de livrare
⚪ [Data] [Ora] - Livrare programată
```

### Detalii Livrare
**Curier:** [Nume curier]
**Telefon curier:** [telefon]
**Interval livrare:** [interval orar]
**Încercări livrare:** [număr]

### Notificări
{f'⚠️ **Atenție:** [problemă detectată]' if 'problemă' else '✅ **Livrare la timp**'}

### Acțiuni Disponibile
- 📞 Contactează curierul
- 📅 Reprogramează livrarea
- 📦 Redirecționează către Easybox
- 🏪 Schimbă la ridicare din punct
"""
        tracking = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Tracking AWB {tracking_number}: {tracking}"])
        return tracking
