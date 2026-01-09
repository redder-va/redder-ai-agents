"""
Agent Live Chat - Răspunde clienților în timp real pe website
Combină capabilitățile mai multor agenți pentru conversații naturale cu date reale din magazin
"""

from agents.llm_helper import generate_text
from services.woocommerce_service import get_woocommerce_service
import os
from datetime import datetime

class LiveChatAgent:
    def __init__(self):
        """Inițializare agent chat live pentru website cu date reale din redder.ro"""
        # Folosește helper-ul existent în loc de genai direct
        self.use_llm_helper = True
        
        # Serviciu WooCommerce pentru date reale
        self.wc = get_woocommerce_service()
        
        # Sincronizează produsele la inițializare
        self.wc.sync_products()

    def chat(self, user_message: str, conversation_history: list = None) -> dict:
        """
        Procesează mesaj client și returnează răspuns cu date reale din magazin
        
        Args:
            user_message: Mesajul clientului
            conversation_history: Lista cu conversații anterioare
            
        Returns:
            dict cu răspuns, produse reale, comparații, rețete
        """
        try:
            # Sincronizează produse dacă e necesar
            self.wc.sync_products()
            
            # Detectează intent
            intent = self._detect_intent(user_message)
            
            # Construiește context cu date reale
            real_data_context = self._build_real_data_context(user_message, intent)
            
            # Construiește prompt complet
            if conversation_history is None:
                conversation_history = []
            
            full_prompt = self._build_system_prompt(real_data_context)
            
            # Adaugă istoric
            if conversation_history:
                full_prompt += "\n\nCONVERSAȚIE ANTERIOARĂ:\n"
                for msg in conversation_history[-5:]:  # Ultimele 5 mesaje
                    role = "CLIENT" if msg['role'] == 'user' else "TU"
                    full_prompt += f"{role}: {msg['content']}\n"
                full_prompt += "\n"
            
            full_prompt += f"CLIENT: {user_message}\nTU:"
            
            # Generează răspuns
            agent_response = generate_text(None, full_prompt).strip()
            
            # Extrage produse sugerate din răspuns
            suggested_products = self._extract_real_products(agent_response)
            
            return {
                'success': True,
                'response': agent_response,
                'intent': intent,
                'suggested_products': suggested_products,
                'timestamp': datetime.now().isoformat(),
                'requires_human': self._needs_human_intervention(user_message, agent_response)
            }
            
        except Exception as e:
            return {
                'success': False,
                'response': "Îmi pare rău, am întâmpinat o problemă tehnică. 😔 Te rog încearcă din nou sau contactează-ne la 0763038001.",
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _build_real_data_context(self, user_message: str, intent: str) -> str:
        """Construiește context cu date reale din magazin bazat pe mesajul clientului"""
        context = ""
        
        # Caută produse relevante
        search_terms = self._extract_search_terms(user_message)
        if search_terms:
            products = self.wc.search_products(search_terms)
            if products:
                context += "\n\n**PRODUSE REALE DISPONIBILE ÎN MAGAZIN:**\n"
                for p in products[:10]:  # Max 10 produse
                    stock_status = "✅ ÎN STOC" if p.get('stock_status') == 'instock' else "❌ FĂRĂ STOC"
                    stock_qty = p.get('stock_quantity', 'N/A')
                    context += f"- {p['name']} - {p.get('price', 'N/A')} RON | {stock_status}"
                    if stock_qty != 'N/A':
                        context += f" ({stock_qty} buc.)"
                    context += f" | SKU: {p.get('sku', 'N/A')}\n"
        
        # Dacă se cere comparație
        if 'compar' in user_message.lower() or 'diferență' in user_message.lower():
            vodka_products = self.wc.get_products_by_category('vodca')
            if vodka_products:
                context += "\n\n**VODCA DISPONIBILĂ - PENTRU COMPARAȚIE:**\n"
                for p in vodka_products[:8]:
                    context += f"- {p['name']} - {p.get('price')} RON | "
                    context += f"Gradație: {self._extract_alcohol_percentage(p['name'])}\n"
        
        # Dacă se cer rețete cocktailuri
        if intent == 'recipe_request':
            context += "\n\n**PRODUSE PENTRU COCKTAILURI:**\n"
            context += "- Vodca (pentru Moscow Mule, Cosmopolitan, Bloody Mary)\n"
            context += "- Gin (pentru Gin Tonic, Negroni)\n"
            context += "- Rom (pentru Mojito, Daiquiri)\n"
            context += "- Lichioruri ORO del Sole (pentru cocktailuri aromate)\n"
        
        # Produse cu stoc scăzut (pentru urgență)
        if intent == 'purchase_intent':
            low_stock = self.wc.get_low_stock_products(threshold=5)
            if low_stock:
                context += f"\n\n**⚠️ PRODUSE CU STOC LIMITAT ({len(low_stock)}): Comandă rapid!**\n"
        
        return context
    
    def _extract_search_terms(self, message: str) -> str:
        """Extrage termeni de căutare din mesaj"""
        message_lower = message.lower()
        
        keywords = ['vodca', 'vodka', 'gin', 'rom', 'whisky', 'lichior', 
                   'oro', 'kumaniok', 'valahia', 'pshenoff', 'velicinsky']
        
        for keyword in keywords:
            if keyword in message_lower:
                return keyword
        
        return ""
    
    def _extract_alcohol_percentage(self, product_name: str) -> str:
        """Extrage procentul de alcool din numele produsului"""
        import re
        match = re.search(r'(\d+(?:\.\d+)?)\s*%', product_name)
        return match.group(1) + "%" if match else "N/A"
    
    def _build_system_prompt(self, real_data_context: str) -> str:
        """Construiește prompt-ul de sistem cu date reale"""
        return f"""
Ești asistentul virtual LIVE al magazinului Redder.ro - specialist în băuturi alcoolice premium.

PERSONALITATE:
- Prietenos, profesionist și empatic
- Răspunzi DOAR în limba română
- Stil conversațional dar respectuos  
- Folosești emojis cu moderație (🍾🥃🍹)
- Bazezi răspunsurile STRICT pe datele reale din magazin

**IMPORTANT: Folosește DOAR produsele reale de mai jos. NU inventa produse sau prețuri!**
{real_data_context}

CAPABILITĂȚI SPECIALE:
1. **Comparații produse** - Analizează diferențele între vodka, gin, etc.
2. **Rețete cocktailuri** - Propune rețete cu produse din magazin
3. **Recomandări personalizate** - Bazate pe preferințe client
4. **Verificare stoc** - Status REAL al disponibilității
5. **Sfaturi expert** - Cum se servesc, pairings, ocazii

REGULI STRICTE:
- ✅ Folosește DOAR produsele listate mai sus
- ✅ Verifică ÎNTOTDEAUNA stocul înainte de recomandare
- ✅ Menționează prețul REAL din baza de date
- ❌ NU inventa produse care nu sunt în listă
- ❌ NU garanta disponibilitate dacă stocul = 0

EXEMPLE RĂSPUNSURI:

**Comparație vodka:**
"Avem 3 vodka excelente:
1. Kumaniok 38% - {self._get_price('kumaniok')} RON - Cea mai vândută! Raport calitate/preț fantastic
2. Valahia Gold 40% - {self._get_price('valahia')} RON - Premium românesc, mai tare
3. Pshenoff 40% - {self._get_price('pshenoff')} RON - Clasică, perfectă pentru cocktailuri

Pentru party: Kumaniok
Pentru cadou: Valahia Gold
Pentru mixat: Pshenoff"

**Rețetă cocktail:**
"🍹 Moscow Mule cu Kumaniok:
- 50ml Vodca Kumaniok (avem la {self._get_price('kumaniok')} RON)
- 150ml ginger beer
- 15ml suc lămâie
- Gheață + felii lămâie

Servește în pahar de cupru! 🔥"

TONUL CONVERSAȚIEI:
- Salut: "Bună! 👋 Cu ce te pot ajuta la comandă?"
- Recomandări: "Pentru gustul tău, recomand..."
- Urgență: "Stoc limitat - adaugă în coș acum!"
- Încheiere: "Adaugă în coș și bucură-te de livrare rapidă! 🚚"
"""
    
    def _get_price(self, product_keyword: str) -> str:
        """Obține prețul real al unui produs"""
        products = self.wc.search_products(product_keyword)
        if products:
            return products[0].get('price', '24')
        return '24'
    
    def _extract_real_products(self, response: str) -> list:
        """Extrage produsele reale menționate în răspuns"""
        products = []
        response_lower = response.lower()
        
        # Caută produse în răspuns
        for word in response_lower.split():
            # Caută în WooCommerce
            search_results = self.wc.search_products(word)
            for product in search_results[:3]:  # Max 3 per cuvânt
                if product not in products:
                    products.append({
                        'name': product['name'],
                        'price': product.get('price', 'N/A'),
                        'sku': product.get('sku', 'N/A'),
                        'link': product.get('permalink', ''),
                        'stock_status': product.get('stock_status', 'unknown')
                    })
        
        return products[:5]  # Max 5 produse în răspuns
    
    def _detect_intent(self, message: str) -> str:
        """Detectează intenția clientului"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['compar', 'diferență', 'diferenta', 'versus', 'vs', 'mai bun']):
            return 'product_comparison'
        elif any(word in message_lower for word in ['cocktail', 'rețetă', 'reteta', 'mix', 'cum se face', 'bautura']):
            return 'recipe_request'
        elif any(word in message_lower for word in ['recomandare', 'sugerează', 'sugereza', 'ce să cumpăr', 'ce vodcă', 'ce vodca']):
            return 'product_recommendation'
        elif any(word in message_lower for word in ['comandă', 'comand', 'cumpăr', 'cumpar', 'adaug', 'coș', 'cos']):
            return 'purchase_intent'
        elif any(word in message_lower for word in ['stoc', 'disponibil', 'aveți', 'aveti', 'există', 'exista']):
            return 'stock_inquiry'
        elif any(word in message_lower for word in ['preț', 'pret', 'costă', 'costa', 'bani', 'RON', 'lei']):
            return 'price_inquiry'
        elif any(word in message_lower for word in ['livrare', 'transport', 'când primesc', 'cand primesc', 'curier']):
            return 'shipping_inquiry'
        elif any(word in message_lower for word in ['cadou', 'gift', 'aniversare', 'petrecere', 'party']):
            return 'gift_suggestion'
        else:
            return 'general_inquiry'
    
    def _needs_human_intervention(self, user_message: str, agent_response: str) -> bool:
        """Verifică dacă conversația necesită intervenție umană"""
        escalation_keywords = [
            'reclamație', 'reclamatie', 'plângere', 'plangere', 'nemulțumit', 'nemultumit',
            'ramburs', 'returnare', 'lawyer', 'avocat', 'tribunal', 'fraud', 'înșelătorie', 'inselatorie',
            'manager', 'director', 'șef', 'sef'
        ]
        
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in escalation_keywords)
    
    def get_quick_replies(self, intent: str) -> list:
        """Generează răspunsuri rapide bazate pe intent"""
        quick_replies = {
            'general_inquiry': [
                "Ce produse aveți?",
                "Promoții active?",
                "Info livrare"
            ],
            'product_comparison': [
                "Diferență vodka",
                "Cea mai bună vodcă",
                "Comparație prețuri"
            ],
            'recipe_request': [
                "Rețetă Moscow Mule",
                "Cocktail cu gin",
                "Mix cu lichior"
            ],
            'product_recommendation': [
                "Vodcă pentru cocktailuri",
                "Cadou aniversare",
                "Pentru femei"
            ],
            'purchase_intent': [
                "Adaug în coș",
                "Livrare gratuită?",
                "Timp livrare"
            ],
            'stock_inquiry': [
                "Când revin în stoc?",
                "Alternative similare?",
                "Notificare stoc"
            ],
            'gift_suggestion': [
                "Cadou bărbați",
                "Cadou femei",
                "Set cadou"
            ]
        }
        
        return quick_replies.get(intent, [
            "Spune-mi mai multe",
            "Am o întrebare",
            "Mulțumesc!"
        ])


# Singleton instance
_live_chat_agent = None

def get_live_chat_agent():
    """Returnează instanța singleton a agentului de chat"""
    global _live_chat_agent
    if _live_chat_agent is None:
        _live_chat_agent = LiveChatAgent()
    return _live_chat_agent
