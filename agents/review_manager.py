from memory.vector_store import get_vector_store
from agents.llm_helper import generate_text

class ReviewManagerAgent:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.llm = None  # Use generate_text fallback
        self.role = 'Agent Gestionare Recenzii'
        self.goal = 'Răspunde la recenzii clienți și gestionează reputația online'
        self.backstory = 'Ești un specialist în customer success pentru Redder.ro, care răspunde profesionist la recenzii pozitive și negative, transformă feedback-ul negativ în oportunități și construiește încrederea clienților.'

    def search_responses(self, query):
        docs = self.vector_store.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in docs])

    def respond_to_review(self, review_text):
        knowledge = self.search_responses(review_text)
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Răspunsuri anterioare: {knowledge}. 

Generează un răspuns profesional ÎN ROMÂNĂ la această recenzie: "{review_text}"

Formează răspunsul cu Markdown:
## Răspuns la Recenzie

### Analiza Recenziei
**Sentiment:** [Pozitiv/Neutru/Negativ]
**Categorie:** [Livrare/Produs/Servicii/Altele]

### Răspunsul Recomandat
[Răspuns profesional, empatic și personalizat]

### Acțiuni de Follow-up
- [Acțiune 1]
- [Acțiune 2]

### Notă
[Recomandări pentru îmbunătățire]
"""
        response = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Recenzie și Răspuns: {review_text} | {response}"])
        return response

    def analyze_sentiment(self, reviews_summary):
        knowledge = self.search_responses(reviews_summary)
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Context: {knowledge}. 

Analizează sentimentul recenziilor ÎN ROMÂNĂ: {reviews_summary}

Creează un raport cu tabele Markdown:

## Raport Analiză Recenzii

### Rezumat General
**Rating Mediu:** [X.X/5 stele]
**Număr Total Recenzii:** [număr]

### Distribuție Sentiment

| Sentiment | Număr | Procent | Trend |
|---|---|---|---|
| Foarte Pozitiv (5⭐) | [X] | [Y%] | ↑/↓/→ |
| Pozitiv (4⭐) | [X] | [Y%] | ↑/↓/→ |
| Neutru (3⭐) | [X] | [Y%] | ↑/↓/→ |
| Negativ (2⭐) | [X] | [Y%] | ↑/↓/→ |
| Foarte Negativ (1⭐) | [X] | [Y%] | ↑/↓/→ |

### Teme Principale
**Pozitive:**
- [Temă 1] - [frecvență]
- [Temă 2] - [frecvență]

**Negative:**
- [Problem 1] - [frecvență]
- [Problem 2] - [frecvență]

### Recomandări
1. [Recomandare bazată pe feedback]
2. [Recomandare bazată pe feedback]

### Acțiuni Prioritare
- [ ] [Acțiune urgentă]
- [ ] [Acțiune importantă]
"""
        analysis = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Analiză Recenzii: {analysis}"])
        return analysis
