import json
import os
from memory.vector_store import get_vector_store
from datetime import datetime

class AgentTrainer:
    """Antrenează agenții cu date despre produse"""
    
    def __init__(self):
        self.products_file = 'data/products_training_texts.json'
        self.vector_store = get_vector_store()
        self.training_log = 'data/training_log.json'
    
    def load_products(self):
        """Încarcă produsele pentru training"""
        if not os.path.exists(self.products_file):
            print(f"❌ Fișierul {self.products_file} nu există!")
            print("   Rulează mai întâi: python scraper/product_scraper.py")
            return None
        
        with open(self.products_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Încărcat {data['total_texts']} produse din {data['updated_at']}")
        return data['texts']
    
    def train_agents(self, products):
        """Antrenează agenții cu informații despre produse"""
        print("\n🎓 Pornire training agenți AI...\n")
        
        # Pregătește textele pentru vector store
        texts_to_add = []
        metadatas = []
        
        for product in products:
            # Text principal
            texts_to_add.append(product['text'])
            metadatas.append({
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'type': 'product_info',
                'trained_at': datetime.now().isoformat()
            })
            
            # Adaugă variante de întrebări pentru training contextual
            product_name = product['product_name']
            
            # Întrebări despre disponibilitate
            texts_to_add.append(f"Client întreabă: '{product_name} este disponibil?'\nRăspuns: Verifică în text - {product['text']}")
            metadatas.append({
                'product_id': product['product_id'],
                'type': 'qa_availability'
            })
            
            # Întrebări despre preț
            texts_to_add.append(f"Client întreabă: 'Cât costă {product_name}?'\nRăspuns: Verifică în text - {product['text']}")
            metadatas.append({
                'product_id': product['product_id'],
                'type': 'qa_price'
            })
        
        print(f"📝 Pregătite {len(texts_to_add)} texte pentru training...")
        
        # Adaugă în vector store în batch-uri
        batch_size = 50
        total_batches = (len(texts_to_add) + batch_size - 1) // batch_size
        
        for i in range(0, len(texts_to_add), batch_size):
            batch_texts = texts_to_add[i:i + batch_size]
            batch_metadatas = metadatas[i:i + batch_size]
            
            try:
                self.vector_store.add_texts(batch_texts, metadatas=batch_metadatas)
                batch_num = i // batch_size + 1
                print(f"✅ Batch {batch_num}/{total_batches} adăugat ({len(batch_texts)} texte)")
            except Exception as e:
                print(f"❌ Eroare la batch {i // batch_size + 1}: {str(e)}")
        
        print(f"\n🎉 Training finalizat! Agenții au învățat despre {len(products)} produse!")
        
        # Salvează log training
        self.save_training_log(len(products), len(texts_to_add))
    
    def save_training_log(self, num_products, num_texts):
        """Salvează log-ul de training"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'products_trained': num_products,
            'total_texts_added': num_texts,
            'vector_store_size': 'N/A'  # FAISS nu oferă size direct
        }
        
        # Încarcă log-ul existent
        if os.path.exists(self.training_log):
            with open(self.training_log, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        else:
            log_data = {'training_sessions': []}
        
        log_data['training_sessions'].append(log_entry)
        log_data['last_training'] = log_entry['timestamp']
        
        with open(self.training_log, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 Log training salvat în: {self.training_log}")
    
    def test_knowledge(self, test_queries=None):
        """Testează cunoștințele agenților după training"""
        print("\n🧪 TESTARE CUNOȘTINȚE AGENȚI\n")
        
        if test_queries is None:
            test_queries = [
                "vodka absolut",
                "gin hendricks",
                "cocktail shaker",
                "rom havana",
                "whisky"
            ]
        
        for query in test_queries:
            print(f"🔍 Query: '{query}'")
            results = self.vector_store.similarity_search(query, k=2)
            
            if results:
                print(f"   ✅ Găsite {len(results)} rezultate relevante")
                for i, doc in enumerate(results, 1):
                    content_preview = doc.page_content[:150].replace('\n', ' ')
                    print(f"   {i}. {content_preview}...")
            else:
                print("   ❌ Niciun rezultat găsit")
            print()
    
    def run(self, test=True):
        """Rulează procesul complet de training"""
        print("🚀 ANTRENARE AGENȚI AI - REDDER.RO\n")
        print("=" * 60)
        
        # Încarcă produsele
        products = self.load_products()
        if not products:
            return False
        
        # Antrenează agenții
        self.train_agents(products)
        
        # Test opțional
        if test:
            self.test_knowledge()
        
        print("\n" + "=" * 60)
        print("✅ TRAINING COMPLETAT CU SUCCES!")
        print("\nAgenții tăi AI acum cunosc toate produsele de pe Redder.ro!")
        print("Pot răspunde la întrebări despre:")
        print("  • Disponibilitate produse")
        print("  • Prețuri și oferte")
        print("  • Caracteristici și descrieri")
        print("  • Stocuri și categorii")
        print("  • Recenzii și rating-uri")
        
        return True


if __name__ == '__main__':
    trainer = AgentTrainer()
    trainer.run(test=True)
