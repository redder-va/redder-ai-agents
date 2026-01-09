from memory.vector_store import get_vector_store
from agents.llm_helper import generate_text

class CustomerServiceAgent:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.llm = None  # Use generate_text fallback
        self.role = 'Agent Serviciu Clienți'
        self.goal = 'Răspunde la întrebările clienților 24/7, oferă suport și învață din interacțiuni'
        self.backstory = 'Ești un reprezentant prietenos și bine informat al serviciului clienți pentru Redder.ro, specializat în cocktail-uri și servicii de bar. Înveți din interacțiunile anterioare pentru a îmbunătăți răspunsurile.'

    def search_knowledge_base(self, query):
        results = self.vector_store.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in results])

    def respond(self, message):
        knowledge = self.search_knowledge_base(message)
        prompt = f"Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. Cunoștințe relevante: {knowledge}. Răspunde În ROMÂNĂ la acest mesaj de la client: {message}"
        response = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Client: {message}\nAgent: {response}"])
        return response