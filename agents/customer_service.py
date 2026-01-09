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
        # Optimizat: doar 2 rezultate pentru viteză
        results = self.vector_store.similarity_search(query, k=2)
        return "\n".join([doc.page_content[:300] for doc in results])  # Max 300 chars per result

    def respond(self, message):
        knowledge = self.search_knowledge_base(message)
        # Prompt optimizat - mai scurt și direct
        prompt = f"Ești asistentul Redder.ro (magazin băuturi alcoolice). Răspunde scurt și prietenos în ROMÂNĂ.\n\nContext: {knowledge}\n\nClient: {message}\n\nRăspuns:"
        # Folosește modelul rapid gemini-1.5-flash
        response = generate_text(self.llm, prompt, model='gemini-1.5-flash')
        # Skip vector store add pentru viteză (se poate activa mai târziu pentru învățare)
        # self.vector_store.add_texts([f"Client: {message}\nAgent: {response}"])
        return response