from langchain_openai import ChatOpenAI
from memory.vector_store import get_vector_store
from agents.llm_helper import generate_text
from agents.link_generator import get_link_generator

class MarketingAgent:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.llm = None  # Use generate_text fallback
        self.role = 'Agent Marketing'
        self.goal = 'Crează campanii și recomandări personalizate'
        self.backstory = 'Ești un specialist în marketing strategic pentru Redder.ro, care elaborează campanii și personalizează recomandările bazate pe datele clienților.'

    def search_customer_data(self, query):
        results = self.vector_store.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in results])

    def create_campaign(self, theme):
        knowledge = self.search_customer_data(theme)
        prompt = f"Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. Date clienți: {knowledge}. Proiectează o campanie de marketing În ROMÂNĂ pe această temă: {theme}. Formatează cu Markdown: titluri (##), liste cu strategii, secțiuni structurate."
        campaign = generate_text(self.llm, prompt)
        
        # Adaugă automat linkuri trackabile
        link_gen = get_link_generator()
        campaign_slug = theme.lower().replace(' ', '-')[:30]
        campaign = link_gen.inject_links_in_campaign(campaign, campaign_slug, 'marketing')
        
        self.vector_store.add_texts([f"Campanie: {campaign}"])
        return campaign

    def personalize_recommendation(self, customer_profile):
        knowledge = self.search_customer_data(customer_profile)
        prompt = f"Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. Date clienți: {knowledge}. Personalizează o recomandare În ROMÂNĂ pentru acest profil de client: {customer_profile}"
        recommendation = generate_text(self.llm, prompt)
        return recommendation