from memory.vector_store import get_vector_store
from agents.llm_helper import generate_text
from agents.link_generator import get_link_generator

class SocialMediaAgent:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.llm = None  # Use generate_text fallback
        self.role = 'Agent Social Media'
        self.goal = 'Generează conținut pentru rețele sociale și gestionează prezența online'
        self.backstory = 'Ești un expert în social media pentru Redder.ro, care creează postări captivante, stories și conținut viral pentru Instagram, Facebook și TikTok.'

    def search_posts(self, query):
        docs = self.vector_store.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in docs])

    def create_post(self, platform_and_topic):
        knowledge = self.search_posts(platform_and_topic)
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Postări anterioare: {knowledge}. 

Creează o postare social media ÎN ROMÂNĂ pentru: {platform_and_topic}

Formează răspunsul cu Markdown:
## Postare Social Media

### Platformă
[Instagram/Facebook/TikTok]

### Textul Postării
[Copy captivant, cu emoji-uri și energie]

### Hashtag-uri
#Redder #Cocktails #[alte hashtag-uri relevante]

### Call-to-Action
[CTA clar]

### Idei de Vizual
- [Descriere imagine/video 1]
- [Descriere imagine/video 2]

### Cel mai bun moment de postare
[Zi și oră recomandată]
"""
        post = generate_text(self.llm, prompt)
        
        # Adaugă automat linkuri trackabile
        link_gen = get_link_generator()
        post_slug = platform_and_topic.lower().replace(' ', '-')[:30]
        post = link_gen.inject_links_in_campaign(post, post_slug, 'social')
        
        self.vector_store.add_texts([f"Postare Social Media: {post}"])
        return post

    def generate_content_calendar(self, period):
        knowledge = self.search_posts(period)
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. 
Context: {knowledge}. 

Creează un calendar de conținut social media ÎN ROMÂNĂ pentru: {period}

Folosește tabele Markdown:

## Calendar Conținut Social Media - {period}

| Zi | Platformă | Tip Conținut | Temă | Hashtag Principal |
|---|---|---|---|---|
| Luni | Instagram | Post | [Temă] | #[hashtag] |
| Marți | Facebook | Video | [Temă] | #[hashtag] |
| Miercuri | Instagram Story | Behind-the-scenes | [Temă] | #[hashtag] |
| Joi | TikTok | Tutorial | [Temă] | #[hashtag] |
| Vineri | Instagram Reel | Rețetă | [Temă] | #[hashtag] |
| Sâmbătă | Facebook | Angajament | [Temă] | #[hashtag] |
| Duminică | Instagram | Inspirație | [Temă] | #[hashtag] |

### Note Importante
- [Recomandare 1]
- [Recomandare 2]
"""
        calendar = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Calendar Conținut: {calendar}"])
        return calendar
