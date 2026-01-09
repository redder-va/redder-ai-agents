from memory.vector_store import get_vector_store
from agents.llm_helper import generate_text
import requests
import os

class ContentCreatorAgent:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.llm = None  # Use generate_text fallback
        self.role = 'Agent Creare Conținut'
        self.goal = 'Generează rețete de cocktail-uri și descrieri de produse'
        self.backstory = 'Ești un creator de conținut creativ pentru Redder.ro, specializat în rețete de cocktail-uri și descrieri captivante de produse. Te inspiri din creațiile anterioare.'

    def search_inspiration(self, query):
        results = self.vector_store.similarity_search(query, k=5)
        return "\n".join([doc.page_content for doc in results])

    def generate_recipe(self, ingredients):
        knowledge = self.search_inspiration(ingredients)
        prompt = f"Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. Inspirație: {knowledge}. Creează o rețetă de cocktail În ROMÂNĂ folosind aceste ingrediente: {ingredients}. Formatează răspunsul cu Markdown: titluri (##), liste cu ingrediente și pași numerotați."
        recipe = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Rețetă: {recipe}"])
        return recipe

    def generate_description(self, product):
        knowledge = self.search_inspiration(product)
        prompt = f"Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. Inspirație: {knowledge}. Scrie o descriere captivantă de produs În ROMÂNĂ pentru: {product}"
        description = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Description: {description}"])
        return description

    def post_content(self, content, title, status='draft'):
        # Conectare la WordPress REST API pentru a posta conținut
        try:
            url = "https://redder.ro/wp-json/wp/v2/posts"
            auth = (os.environ.get('WP_USERNAME'), os.environ.get('WP_PASSWORD'))  # Basic Auth sau JWT
            data = {
                'title': title,
                'content': content,
                'status': status
            }
            response = requests.post(url, auth=auth, json=data)
            if response.status_code == 201:
                return "Content posted successfully"
            else:
                return f"Error posting content: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error connecting to WordPress API: {e}"