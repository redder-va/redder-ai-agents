"""
Link Generator pentru campanii marketing
Generează automat linkuri trackabile pentru produse și campanii
"""

import urllib.parse
from typing import Dict, List

class LinkGenerator:
    """Generează linkuri automate pentru campanii marketing"""
    
    def __init__(self):
        self.base_url = "https://redder.ro"
        self.product_categories = {
            "vodka": "/categorie-produs/vodka/",
            "rom": "/categorie-produs/rom/",
            "gin": "/categorie-produs/gin/",
            "whisky": "/categorie-produs/whisky/",
            "tequila": "/categorie-produs/tequila/",
            "cocktail": "/categorie-produs/cocktailuri/",
            "lichior": "/categorie-produs/lichioruri/",
            "vin": "/categorie-produs/vinuri/",
            "sampanie": "/categorie-produs/sampanii/",
            "bauturi": "/magazin/"
        }
        
        self.campaign_actions = {
            "cumpara": "shop-now",
            "descopera": "discover",
            "exploreaza": "explore",
            "vezi-oferta": "view-offer",
            "comanda": "order-now",
            "rezerva": "reserve"
        }
    
    def generate_campaign_link(self, category: str = "magazin", campaign_name: str = "campanie", 
                              medium: str = "email", action: str = "cumpara") -> str:
        """
        Generează link trackabil pentru campanie
        
        Args:
            category: Categoria produsului (vodka, rom, gin, etc.)
            campaign_name: Numele campaniei (fara spatii)
            medium: Mediul (email, social, newsletter)
            action: Acțiunea (cumpara, descopera, etc.)
        
        Returns:
            URL complet cu parametri UTM
        """
        # Normalizează categoria
        category = category.lower().strip()
        page_path = self.product_categories.get(category, "/magazin/")
        
        # Normalizează numele campaniei
        campaign_slug = campaign_name.lower().replace(" ", "-").replace("ă", "a").replace("â", "a").replace("î", "i").replace("ș", "s").replace("ț", "t")
        
        # Parametri UTM
        utm_params = {
            "utm_source": "ai-agent",
            "utm_medium": medium,
            "utm_campaign": campaign_slug,
            "utm_content": self.campaign_actions.get(action, action)
        }
        
        # Construiește URL-ul
        query_string = urllib.parse.urlencode(utm_params)
        full_url = f"{self.base_url}{page_path}?{query_string}"
        
        return full_url
    
    def generate_product_links(self, products: List[str], campaign_name: str = "recomandare", 
                               medium: str = "email") -> Dict[str, str]:
        """
        Generează linkuri pentru o listă de produse
        
        Args:
            products: Lista de produse/categorii
            campaign_name: Numele campaniei
            medium: Mediul de promovare
        
        Returns:
            Dict cu produsul și linkul său
        """
        links = {}
        for product in products:
            # Încearcă să găsească categoria din numele produsului
            category = "magazin"
            product_lower = product.lower()
            for cat_key in self.product_categories.keys():
                if cat_key in product_lower:
                    category = cat_key
                    break
            
            links[product] = self.generate_campaign_link(
                category=category,
                campaign_name=campaign_name,
                medium=medium,
                action="cumpara"
            )
        
        return links
    
    def get_cta_button(self, text: str = "Cumpără Acum", category: str = "magazin", 
                      campaign_name: str = "campanie", medium: str = "email") -> str:
        """
        Generează un button Markdown cu link trackabil
        
        Returns:
            String Markdown pentru button/link
        """
        link = self.generate_campaign_link(category, campaign_name, medium, "cumpara")
        return f"[{text}]({link})"
    
    def get_category_links_markdown(self, campaign_name: str = "campanie", 
                                    medium: str = "email") -> str:
        """
        Generează un set de linkuri pentru toate categoriile în format Markdown
        
        Returns:
            String Markdown cu linkuri pentru categorii
        """
        links_md = "### 🔗 Linkuri Rapide:\n\n"
        
        categories_display = {
            "vodka": "🍸 Vodka",
            "rom": "🥃 Rom",
            "gin": "🍹 Gin",
            "whisky": "🥃 Whisky",
            "cocktail": "🍹 Cocktail-uri",
            "bauturi": "🛒 Tot Magazinul"
        }
        
        for cat_key, display_name in categories_display.items():
            link = self.generate_campaign_link(cat_key, campaign_name, medium, "descopera")
            links_md += f"- [{display_name}]({link})\n"
        
        return links_md
    
    def inject_links_in_campaign(self, campaign_text: str, campaign_name: str = "campanie",
                                 medium: str = "email") -> str:
        """
        Inserează automat linkuri într-un text de campanie
        Caută cuvinte cheie și adaugă linkuri relevante
        
        Args:
            campaign_text: Textul campaniei
            campaign_name: Numele campaniei pentru tracking
            medium: Mediul (email, social, etc.)
        
        Returns:
            Text cu linkuri inserate
        """
        # Adaugă linkuri la sfârșitul campaniei
        campaign_with_links = campaign_text + "\n\n---\n\n"
        campaign_with_links += self.get_category_links_markdown(campaign_name, medium)
        
        # Adaugă CTA principal
        campaign_with_links += f"\n\n{self.get_cta_button('🛒 Cumpără Acum', 'magazin', campaign_name, medium)}\n"
        
        return campaign_with_links


# Singleton instance
_link_generator = None

def get_link_generator() -> LinkGenerator:
    """Obține instanța singleton a generatorului de linkuri"""
    global _link_generator
    if _link_generator is None:
        _link_generator = LinkGenerator()
    return _link_generator
