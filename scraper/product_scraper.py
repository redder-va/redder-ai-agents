import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class ProductScraper:
    """Extrage produse din WooCommerce API și le salvează pentru training"""
    
    def __init__(self):
        self.wc_url = os.getenv('WC_URL', 'https://redder.ro')
        self.consumer_key = os.getenv('WC_CONSUMER_KEY', '')
        self.consumer_secret = os.getenv('WC_CONSUMER_SECRET', '')
        self.products_file = 'data/products_training.json'
        
        # Crează directorul data dacă nu există
        os.makedirs('data', exist_ok=True)
    
    def fetch_all_products(self):
        """Extrage toate produsele din WooCommerce"""
        print("🔄 Conectare la WooCommerce API...")
        
        all_products = []
        page = 1
        per_page = 100
        
        try:
            while True:
                url = f"{self.wc_url}/wp-json/wc/v3/products"
                params = {
                    'per_page': per_page,
                    'page': page,
                    'status': 'publish'
                }
                
                response = requests.get(
                    url,
                    params=params,
                    auth=(self.consumer_key, self.consumer_secret),
                    timeout=30
                )
                
                if response.status_code != 200:
                    print(f"❌ Eroare API: {response.status_code}")
                    break
                
                products = response.json()
                
                if not products:
                    break
                
                all_products.extend(products)
                print(f"✅ Pagina {page}: {len(products)} produse extrase")
                
                page += 1
                
                # Verifică dacă mai sunt produse
                if len(products) < per_page:
                    break
            
            print(f"\n🎉 Total produse extrase: {len(all_products)}")
            return all_products
            
        except Exception as e:
            print(f"❌ Eroare la extragere produse: {str(e)}")
            return []
    
    def process_product(self, product):
        """Procesează un produs și extrage informații relevante"""
        
        # Extrage categorii
        categories = [cat['name'] for cat in product.get('categories', [])]
        
        # Extrage atribute (pentru cocktail ingredients, etc.)
        attributes = {}
        for attr in product.get('attributes', []):
            attributes[attr.get('name', '')] = attr.get('options', [])
        
        # Extrage meta data
        meta_data = {}
        for meta in product.get('meta_data', []):
            key = meta.get('key', '')
            if not key.startswith('_'):  # Skip private meta
                meta_data[key] = meta.get('value', '')
        
        return {
            'id': product.get('id'),
            'name': product.get('name', ''),
            'slug': product.get('slug', ''),
            'description': product.get('description', ''),
            'short_description': product.get('short_description', ''),
            'price': product.get('price', ''),
            'regular_price': product.get('regular_price', ''),
            'sale_price': product.get('sale_price', ''),
            'stock_status': product.get('stock_status', ''),
            'stock_quantity': product.get('stock_quantity'),
            'categories': categories,
            'tags': [tag['name'] for tag in product.get('tags', [])],
            'attributes': attributes,
            'images': [img['src'] for img in product.get('images', [])],
            'rating_count': product.get('rating_count', 0),
            'average_rating': product.get('average_rating', '0'),
            'meta_data': meta_data,
            'sku': product.get('sku', ''),
            'weight': product.get('weight', ''),
            'dimensions': product.get('dimensions', {}),
        }
    
    def create_training_text(self, product):
        """Creează text formatat pentru training agenți"""
        
        text_parts = []
        
        # Titlu și categorii
        text_parts.append(f"Produs: {product['name']}")
        if product['categories']:
            text_parts.append(f"Categorii: {', '.join(product['categories'])}")
        
        # Preț
        if product['sale_price']:
            text_parts.append(f"Preț: {product['sale_price']} RON (redus de la {product['regular_price']} RON)")
        elif product['price']:
            text_parts.append(f"Preț: {product['price']} RON")
        
        # SKU
        if product['sku']:
            text_parts.append(f"Cod produs: {product['sku']}")
        
        # Descriere scurtă
        if product['short_description']:
            # Remove HTML tags
            import re
            clean_desc = re.sub('<.*?>', '', product['short_description'])
            text_parts.append(f"Descriere scurtă: {clean_desc.strip()}")
        
        # Descriere completă
        if product['description']:
            import re
            clean_desc = re.sub('<.*?>', '', product['description'])
            text_parts.append(f"Descriere: {clean_desc.strip()}")
        
        # Atribute
        if product['attributes']:
            for attr_name, attr_values in product['attributes'].items():
                if attr_values:
                    text_parts.append(f"{attr_name}: {', '.join(attr_values)}")
        
        # Stock
        if product['stock_status'] == 'instock':
            if product['stock_quantity']:
                text_parts.append(f"Stoc: {product['stock_quantity']} bucăți disponibile")
            else:
                text_parts.append("Stoc: Disponibil")
        else:
            text_parts.append("Stoc: Indisponibil momentan")
        
        # Rating
        if product['rating_count'] > 0:
            text_parts.append(f"Rating: {product['average_rating']}/5 ({product['rating_count']} recenzii)")
        
        # Tags
        if product['tags']:
            text_parts.append(f"Etichete: {', '.join(product['tags'])}")
        
        return "\n".join(text_parts)
    
    def save_products(self, products):
        """Salvează produsele procesate"""
        processed_products = []
        training_texts = []
        
        for product in products:
            processed = self.process_product(product)
            processed_products.append(processed)
            
            # Creează text pentru training
            training_text = self.create_training_text(processed)
            training_texts.append({
                'product_id': processed['id'],
                'product_name': processed['name'],
                'text': training_text
            })
        
        # Salvează produsele complete
        with open(self.products_file, 'w', encoding='utf-8') as f:
            json.dump({
                'updated_at': datetime.now().isoformat(),
                'total_products': len(processed_products),
                'products': processed_products
            }, f, ensure_ascii=False, indent=2)
        
        # Salvează texte pentru training
        training_file = 'data/products_training_texts.json'
        with open(training_file, 'w', encoding='utf-8') as f:
            json.dump({
                'updated_at': datetime.now().isoformat(),
                'total_texts': len(training_texts),
                'texts': training_texts
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Produse salvate în: {self.products_file}")
        print(f"💾 Texte training salvate în: {training_file}")
        
        return processed_products, training_texts
    
    def run(self):
        """Rulează procesul complet de extragere și salvare"""
        print("🚀 Pornire Product Scraper pentru Redder.ro\n")
        
        # Extrage produse
        products = self.fetch_all_products()
        
        if not products:
            print("❌ Nu s-au extras produse. Verifică credențialele WooCommerce.")
            return False
        
        # Procesează și salvează
        processed, training_texts = self.save_products(products)
        
        # Statistici
        print("\n📊 STATISTICI:")
        print(f"   Total produse: {len(processed)}")
        
        # Categorii
        all_categories = set()
        for p in processed:
            all_categories.update(p['categories'])
        print(f"   Categorii unice: {len(all_categories)}")
        
        # Stoc
        in_stock = sum(1 for p in processed if p['stock_status'] == 'instock')
        print(f"   Produse în stoc: {in_stock}/{len(processed)}")
        
        # Cu recenzii
        with_reviews = sum(1 for p in processed if p['rating_count'] > 0)
        print(f"   Produse cu recenzii: {with_reviews}")
        
        print("\n✅ Scraping finalizat cu succes!")
        return True


if __name__ == '__main__':
    scraper = ProductScraper()
    scraper.run()
