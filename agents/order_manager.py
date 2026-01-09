from memory.vector_store import get_vector_store
from agents.llm_helper import generate_text
from woocommerce import API
import os

class OrderManagerAgent:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.llm = None
        self.role = 'Agent Gestionare Comenzi'
        self.goal = 'Procesează și urmărește comenzi, automatizează workflow-ul de comenzi'
        self.backstory = 'Ești un manager de comenzi eficient pentru Redder.ro, care procesează comenzi 24/7, verifică statusuri, detectează probleme și asigură livrarea la timp.'
        
        # WooCommerce API
        self.wc_api = API(
            url=os.getenv('WC_URL', 'https://redder.ro'),
            consumer_key=os.getenv('WC_CONSUMER_KEY', ''),
            consumer_secret=os.getenv('WC_CONSUMER_SECRET', ''),
            version="wc/v3"
        )

    def search_order_history(self, query):
        docs = self.vector_store.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in docs])

    def process_order(self, order_details):
        knowledge = self.search_order_history(order_details)
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Istoric comenzi: {knowledge}. 

Procesează această comandă ÎN ROMÂNĂ: {order_details}

Creează un raport cu Markdown:

## Procesare Comandă

### Detalii Comandă
**Număr Comandă:** #[număr]
**Client:** [nume]
**Total:** [suma] RON
**Status:** [status]

### Produse
| Produs | Cantitate | Preț Unitar | Subtotal |
|---|---|---|---|
| [Produs 1] | [cant] | [preț] RON | [total] RON |
| [Produs 2] | [cant] | [preț] RON | [total] RON |

### Verificări Automate
- [ ] Stoc disponibil - ✅/❌
- [ ] Adresă validă - ✅/❌
- [ ] Plată procesată - ✅/❌
- [ ] Metodă livrare confirmată - ✅/❌

### Acțiuni Următoare
1. [Acțiune 1]
2. [Acțiune 2]

### Estimare Procesare
**Timp estimat pregătire:** [X] ore
**Data livrare estimată:** [data]
"""
        response = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Comandă procesată: {response}"])
        return response

    def track_order(self, order_id):
        try:
            # Încearcă să obții comanda din WooCommerce
            order = self.wc_api.get(f"orders/{order_id}").json()
            
            prompt = f"""Tu ești {self.role}. {self.backstory}. 

Generează un raport de tracking ÎN ROMÂNĂ pentru această comandă:
- Număr: #{order.get('number', order_id)}
- Status: {order.get('status', 'necunoscut')}
- Total: {order.get('total', '0')} RON
- Data: {order.get('date_created', 'N/A')}

Folosește Markdown cu emoji pentru vizualizare:

## 📦 Tracking Comandă #{order.get('number', order_id)}

### Status Curent: {order.get('status', 'necunoscut').upper()}

### Cronologie
🔵 **Comandă Plasată** - {order.get('date_created', 'N/A')}
{'🟢 **Comandă Confirmată** - [data]' if order.get('status') in ['processing', 'completed'] else '⚪ Comandă Confirmată - în așteptare'}
{'🟡 **În Pregătire** - [data]' if order.get('status') == 'processing' else '⚪ În Pregătire - în așteptare'}
{'🟠 **Expediată** - [data]' if order.get('status') in ['completed', 'shipped'] else '⚪ Expediată - în așteptare'}
{'🟢 **Livrată** - [data]' if order.get('status') == 'completed' else '⚪ Livrată - în așteptare'}

### Detalii Livrare
**Adresă:** {order.get('shipping', {}).get('address_1', 'N/A')}
**Oraș:** {order.get('shipping', {}).get('city', 'N/A')}
**Județ:** {order.get('shipping', {}).get('state', 'N/A')}

### Contact
**Nume:** {order.get('billing', {}).get('first_name', '')} {order.get('billing', {}).get('last_name', '')}
**Telefon:** {order.get('billing', {}).get('phone', 'N/A')}
**Email:** {order.get('billing', {}).get('email', 'N/A')}
"""
            tracking = generate_text(self.llm, prompt)
            self.vector_store.add_texts([f"Tracking comandă #{order_id}: {tracking}"])
            return tracking
            
        except Exception as e:
            return f"## Eroare Tracking\n\nNu am putut accesa comanda #{order_id}. Verifică numărul comenzii.\n\n**Detalii eroare:** {str(e)}"

    def detect_issues(self, time_period):
        knowledge = self.search_order_history(f"probleme comenzi {time_period}")
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Date istoric: {knowledge}. 

Analizează și detectează probleme în comenzile din perioada ÎN ROMÂNĂ: {time_period}

Creează raport cu tabele Markdown:

## 🚨 Raport Probleme Comenzi - {time_period}

### Rezumat
**Total comenzi analizate:** [număr]
**Comenzi cu probleme:** [număr] ([procent]%)

### Tipuri Probleme Detectate

| Tip Problemă | Frecvență | Severitate | Impact |
|---|---|---|---|
| Întârzieri livrare | [X] | 🔴/🟡/🟢 | [impact] |
| Lipsă stoc | [X] | 🔴/🟡/🟢 | [impact] |
| Erori plată | [X] | 🔴/🟡/🟢 | [impact] |
| Adrese incorecte | [X] | 🔴/🟡/🟢 | [impact] |
| Retururi | [X] | 🔴/🟡/🟢 | [impact] |

### Acțiuni Recomandate (Prioritate)
1. 🔴 **Urgentă:** [Acțiune critică]
2. 🟡 **Importantă:** [Acțiune importantă]
3. 🟢 **Îmbunătățire:** [Acțiune preventivă]

### Tendințe
[Observații despre pattern-uri și tendințe]
"""
        analysis = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Analiză probleme: {analysis}"])
        return analysis
