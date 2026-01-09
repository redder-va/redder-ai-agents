from langchain_openai import ChatOpenAI
from memory.vector_store import get_vector_store
from agents.llm_helper import generate_text
from services.woocommerce_service import get_woocommerce_service
import os

class InventoryManagerAgent:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.llm = None  # Use generate_text fallback
        self.role = 'Agent Gestionare Stoc'
        self.goal = 'Monitorizează stocurile și sugerează comenzi de pe redder.ro'
        self.backstory = 'Ești un manager de inventar eficient pentru Redder.ro, care urmărește nivelurile de stoc în timp real și optimizează comenzile bazate pe date actuale din magazin.'
        # Serviciu WooCommerce centralizat
        self.wc = get_woocommerce_service()

    def check_stock_levels(self, item):
        """Verifică stocul unui produs de pe redder.ro"""
        # Sincronizare produse
        self.wc.sync_products()
        
        # Caută produsul
        products = self.wc.search_products(item)
        
        if not products:
            # Încearcă producte cu stoc scăzut
            low_stock = self.wc.get_low_stock_products()
            return f"❌ Produs '{item}' nu a fost găsit. Produse cu stoc scăzut: {len(low_stock)}"
        
        product = products[0]
        stock_info = self.wc.get_stock_status(product_id=product['id'])
        
        status_icon = "✅" if stock_info['in_stock'] else "❌"
        
        result = f"""
{status_icon} **{product['name']}**
**SKU:** {stock_info['sku']}
**Stoc disponibil:** {stock_info['stock_quantity']} bucăți
**Status:** {stock_info['stock_status']}
**Preț:** {product.get('price', 'N/A')} RON
**Link:** {product.get('permalink', 'N/A')}
"""
        return result.strip()

    def suggest_order(self, item):
        """Sugerează comandă bazată pe stocuri actuale de pe redder.ro"""
        # Obține date reale
        self.wc.sync_products()
        stock_info = self.check_stock_levels(item)
        low_stock = self.wc.get_low_stock_products(threshold=10)
        out_of_stock = self.wc.get_out_of_stock_products()
        
        knowledge = "\n".join([doc.page_content for doc in self.vector_store.similarity_search(item, k=3)])
        
        prompt = f"""Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}.

**Date anterioare:** {knowledge}

**Status stoc curent:**
{stock_info}

**Produse cu stoc scăzut (sub 10 bucăți):** {len(low_stock)}
**Produse fără stoc:** {len(out_of_stock)}

Sugerează cantitate de comandat pentru '{item}' ÎN ROMÂNĂ, bazat strict pe:
1. Stocul actual din magazin
2. Tendințe vânzări
3. Sezonalitate

Formează răspuns cu Markdown:
## Sugestie Comandă {item}
### Analiză Stoc
[Analiză detaliată]
### Cantitate Recomandată
[Cantitate + justificare]
### Costuri Estimate
[Calcule]
"""
        suggestion = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Sugestie Comandă: {suggestion}"])
        return suggestion