from memory.vector_store import get_vector_store
from agents.llm_helper import generate_text

class LoyaltyManagerAgent:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.llm = None
        self.role = 'Agent Fidelizare Clienți'
        self.goal = 'Gestionează programe de loialitate, recompense și engagement clienți'
        self.backstory = 'Ești un specialist în customer retention pentru Redder.ro, care creează programe de fidelizare, acordă puncte și recompense, și transformă clienții ocazionali în clienți fideli.'

    def search_loyalty_data(self, query):
        docs = self.vector_store.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in docs])

    def calculate_points(self, customer_activity):
        knowledge = self.search_loyalty_data(customer_activity)
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Date loialitate: {knowledge}. 

Calculează punctele de loialitate ÎN ROMÂNĂ pentru: {customer_activity}

Creează raport cu Markdown:

## 🌟 Raport Puncte Loialitate

### Activitate Client
**Perioada:** [perioadă]
**Nume client:** [nume]
**Nivel membru:** [Bronze/Silver/Gold/Platinum]

### Calcul Puncte

| Activitate | Detalii | Puncte Câștigate | Data |
|---|---|---|---|
| Achiziție | Comandă #[id] - [suma] RON | +[X] puncte | [data] |
| Review produs | [Produs] - 5⭐ | +50 puncte | [data] |
| Recomandare | Client nou #[id] | +100 puncte | [data] |
| Social Media | Share Instagram | +25 puncte | [data] |
| Newsletter | Citit și click | +10 puncte | [data] |

### Total Puncte
**Sold anterior:** [X] puncte
**Câștigate perioada:** +[Y] puncte
**Utilizate:** -[Z] puncte
**Sold curent:** **[Total] puncte** 🎉

### Recompense Disponibile
- [ ] **100 puncte** = 10 RON discount
- [ ] **500 puncte** = Transport gratuit (1 lună)
- [ ] **1000 puncte** = Cocktail gratuit la alegere
- [ ] **2500 puncte** = Upgrade la Gold Member
- [x] **5000 puncte** = Set premium bar tools (DEBLOCATĂ!)

### Până la Următorul Nivel
**Progres către [nivel următor]:**
```
████████░░░░░░░░░░ 45% ([X]/[Y] puncte)
```
**Mai trebuie:** [diferență] puncte

### Oferte Personalizate
{f'🎁 **Bonus Special:** Dublează punctele în următoarele 48h!'}
"""
        points = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Puncte loialitate: {points}"])
        return points

    def create_vip_program(self, customer_segment):
        knowledge = self.search_loyalty_data("program VIP")
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Date programe: {knowledge}. 

Creează un program VIP personalizat ÎN ROMÂNĂ pentru: {customer_segment}

Folosește Markdown elegant:

## 👑 Program VIP Redder.ro

### Niveluri Membru

#### 🥉 Bronze (Start)
**Condiții:** Client înregistrat
**Beneficii:**
- 5% discount la toate produsele
- 1 punct / 10 RON cheltuit
- Newsletter exclusiv cu rețete
- Acces early la reduceri

#### 🥈 Silver (500 puncte sau 1000 RON/an)
**Beneficii Bronze PLUS:**
- 10% discount permanent
- 2 puncte / 10 RON cheltuit
- Transport gratuit comenzi >150 RON
- Cadou de ziua de naștere
- Acces la evenimente bartending

#### 🥇 Gold (2000 puncte sau 5000 RON/an)
**Beneficii Silver PLUS:**
- 15% discount permanent
- 3 puncte / 10 RON cheltuit
- Transport gratuit toate comenzile
- Serviciu clienți prioritar
- Consultanță personalizată cocktail-uri
- Invitații exclusive la degustări

#### 💎 Platinum (10000 puncte sau 15000 RON/an)
**Beneficii Gold PLUS:**
- 20% discount permanent
- 5 puncte / 10 RON cheltuit
- Personal shopper dedicat
- Livrare în 24h garantată
- Retur gratuit 60 zile
- Acces la produse limited edition
- Workshop privat bartending (anual)

### Modul de Câștigare Puncte

| Activitate | Puncte | Detalii |
|---|---|---|
| Achiziție | 1-5 / 10 RON | Depinde de nivel |
| Review cu foto | 100 puncte | Pentru fiecare produs |
| Recomandare cu succes | 200 puncte | Când prietenul comandă |
| Share social media | 50 puncte | Post cu tag @redder.ro |
| Completare profil | 150 puncte | O singură dată |
| Participare sondaj | 75 puncte | Lunar |

### Oferte Exclusive VIP - {customer_segment}
[Oferte personalizate bazate pe segment]

### Cum Te Înscrii
1. Creează cont pe Redder.ro
2. Plasează prima comandă
3. Primești automat status Bronze
4. Acumulează puncte și avansează!
"""
        program = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Program VIP: {program}"])
        return program

    def suggest_rewards(self, customer_profile):
        knowledge = self.search_loyalty_data(customer_profile)
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Profil client: {knowledge}. 

Sugerează recompense personalizate ÎN ROMÂNĂ pentru: {customer_profile}

Creează oferte cu Markdown:

## 🎁 Recompense Personalizate Pentru Tine

### Bazate pe Preferințele Tale
[Analiza preferințelor din istoric comenzi]

### Recompense Recomandate

#### 🌟 Recomandarea #1
**Titlu:** [Numele recompensei]
**Cost:** [X] puncte sau [Y] RON
**De ce pentru tine:** [Motivație personalizată]
**Economisești:** [suma] RON
**Valabil până:** [data]

#### ⭐ Recomandarea #2
[Similar...]

#### ⭐ Recomandarea #3
[Similar...]

### Oferte pe Termen Limitat
```
⏰ Expiră în: [timp rămas]
```
- 🔥 **Flash Deal:** [Ofertă urgentă]
- 🎉 **Weekend Special:** [Ofertă weekend]

### Câștigă Puncte Extra
**Provocări active:**
- [ ] Comandă 3 produse diferite → +300 puncte
- [ ] Lasă 5 review-uri → +250 puncte
- [ ] Recomandă 2 prieteni → +400 puncte

### Istoric Recompense
[Lista recompenselor utilizate anterior]
"""
        rewards = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Recompense sugerate: {rewards}"])
        return rewards
