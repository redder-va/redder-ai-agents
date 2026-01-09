from memory.vector_store import get_vector_store
from agents.llm_helper import generate_text
from agents.link_generator import get_link_generator

class EmailMarketingAgent:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.llm = None  # Use generate_text fallback
        self.role = 'Agent Email Marketing'
        self.goal = 'Creează campanii email personalizate și newsletter-e'
        self.backstory = 'Ești un specialist în email marketing pentru Redder.ro, care creează campanii personalizate, newsletter-e și secvențe automate de email-uri pentru a crește engagement-ul clienților.'

    def search_campaigns(self, query):
        docs = self.vector_store.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in docs])

    def create_email_campaign(self, campaign_type):
        knowledge = self.search_campaigns(campaign_type)
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Campanii anterioare: {knowledge}. 

Creează o campanie email ÎN ROMÂNĂ pentru: {campaign_type}

Formează răspunsul cu Markdown:
## Titlu Campanie
**Subiect Email:** (catchy subject line)
**Preview Text:** (preheader text)

### Conținut Email
[Corpul email-ului - personalizat, convingător]

### Call-to-Action
[CTA clar]

### Segment țintă
[Descriere audiență]

### Metrici de urmărit
- [Metric 1]
- [Metric 2]
"""
        campaign = generate_text(self.llm, prompt)
        
        # Adaugă automat linkuri trackabile
        link_gen = get_link_generator()
        campaign_slug = campaign_type.lower().replace(' ', '-')[:30]
        campaign = link_gen.inject_links_in_campaign(campaign, campaign_slug, 'email')
        
        self.vector_store.add_texts([f"Campanie Email: {campaign}"])
        return campaign

    def generate_newsletter(self, topic):
        knowledge = self.search_campaigns(topic)
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Context: {knowledge}. 

Generează un newsletter ÎN ROMÂNĂ despre: {topic}

Folosește Markdown pentru formatare:
## Newsletter Redder.ro

### Titlu Principal
[Headline captivant]

### Articol Principal
[Conținut interesant despre cocktail-uri/bar]

### Produse Recomandate
- **Produs 1:** Descriere
- **Produs 2:** Descriere

### Tips & Tricks
[Sfaturi utile]

### Oferte Speciale
[Promoții curente]
"""
        newsletter = generate_text(self.llm, prompt)
        
        # Adaugă automat linkuri trackabile
        link_gen = get_link_generator()
        newsletter_slug = topic.lower().replace(' ', '-')[:30]
        newsletter = link_gen.inject_links_in_campaign(newsletter, newsletter_slug, 'newsletter')
        
        self.vector_store.add_texts([f"Newsletter: {newsletter}"])
        return newsletter
