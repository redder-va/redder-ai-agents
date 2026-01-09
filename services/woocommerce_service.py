"""
Serviciu WooCommerce - Sincronizare automată cu magazinul redder.ro
Gestionează produse, stocuri, comenzi și date în timp real
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from woocommerce import API
from threading import Lock
import logging

logger = logging.getLogger(__name__)

class WooCommerceService:
    """Serviciu central pentru sincronizare cu WooCommerce redder.ro"""
    
    def __init__(self):
        self.api = None
        self.products_cache = []
        self.categories_cache = []
        self.last_sync = None
        self.cache_duration = timedelta(minutes=15)  # Cache 15 minute
        self.lock = Lock()
        
        # Inițializare conexiune
        self._init_api()
    
    def _init_api(self):
        """Inițializează conexiunea cu WooCommerce API"""
        try:
            wc_url = os.environ.get('WOOCOMMERCE_URL', 'https://redder.ro')
            wc_key = os.environ.get('WOOCOMMERCE_KEY', '')
            wc_secret = os.environ.get('WOOCOMMERCE_SECRET', '')
            
            if not wc_key or not wc_secret:
                # Încearcă și vechile variabile
                wc_key = os.environ.get('WC_CONSUMER_KEY', '')
                wc_secret = os.environ.get('WC_CONSUMER_SECRET', '')
            
            if wc_key and wc_secret:
                self.api = API(
                    url=wc_url,
                    consumer_key=wc_key,
                    consumer_secret=wc_secret,
                    version="wc/v3",
                    timeout=10  # Timeout redus la 10 secunde
                )
                logger.info(f"WooCommerce API conectat la {wc_url}")
            else:
                logger.warning("WooCommerce API credentials not configured")
        except Exception as e:
            logger.error(f"Eroare inițializare WooCommerce API: {e}")
    
    def is_connected(self) -> bool:
        """Verifică dacă API-ul este conectat"""
        return self.api is not None
    
    def needs_refresh(self) -> bool:
        """Verifică dacă cache-ul trebuie actualizat"""
        if not self.last_sync:
            return True
        return datetime.now() - self.last_sync > self.cache_duration
    
    def sync_products(self, force: bool = False) -> List[Dict]:
        """
        Sincronizează lista de produse din WooCommerce
        
        Args:
            force: Forțează sincronizarea chiar dacă cache-ul e valid
        
        Returns:
            Lista de produse actualizată
        """
        with self.lock:
            if not force and not self.needs_refresh() and self.products_cache:
                logger.info(f"Folosesc cache produse ({len(self.products_cache)} produse)")
                return self.products_cache
            
            if not self.is_connected():
                logger.warning("WooCommerce API nu este conectat")
                return self.products_cache
            
            try:
                logger.info("Sincronizare produse din redder.ro...")
                all_products = []
                page = 1
                per_page = 100
                
                while True:
                    response = self.api.get("products", params={
                        "per_page": per_page,
                        "page": page,
                        "status": "publish"
                    })
                    
                    products = response.json()
                    if not products:
                        break
                    
                    all_products.extend(products)
                    page += 1
                    
                    # Limită de siguranță
                    if page > 50:
                        break
                
                self.products_cache = all_products
                self.last_sync = datetime.now()
                
                logger.info(f"✅ Sincronizat {len(all_products)} produse de pe redder.ro")
                return all_products
                
            except Exception as e:
                logger.error(f"Eroare sincronizare produse: {e}")
                return self.products_cache
    
    def get_product_by_sku(self, sku: str) -> Optional[Dict]:
        """Caută produs după SKU"""
        if not self.is_connected():
            return None
        
        try:
            response = self.api.get("products", params={"sku": sku})
            products = response.json()
            return products[0] if products else None
        except Exception as e:
            logger.error(f"Eroare căutare produs SKU {sku}: {e}")
            return None
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """Obține produs după ID"""
        if not self.is_connected():
            return None
        
        try:
            response = self.api.get(f"products/{product_id}")
            return response.json()
        except Exception as e:
            logger.error(f"Eroare obținere produs {product_id}: {e}")
            return None
    
    def get_stock_status(self, product_id: int = None, sku: str = None) -> Dict:
        """
        Obține status stoc pentru produs
        
        Returns:
            Dict cu stock_quantity, stock_status, manage_stock
        """
        product = None
        
        if sku:
            product = self.get_product_by_sku(sku)
        elif product_id:
            product = self.get_product_by_id(product_id)
        
        if not product:
            return {
                "stock_quantity": 0,
                "stock_status": "outofstock",
                "manage_stock": False,
                "in_stock": False
            }
        
        return {
            "stock_quantity": product.get("stock_quantity", 0),
            "stock_status": product.get("stock_status", "outofstock"),
            "manage_stock": product.get("manage_stock", False),
            "in_stock": product.get("stock_status") == "instock",
            "backorders": product.get("backorders", "no"),
            "name": product.get("name", ""),
            "sku": product.get("sku", "")
        }
    
    def get_products_by_category(self, category_slug: str) -> List[Dict]:
        """Obține produse dintr-o categorie specifică"""
        products = self.sync_products()
        
        category_products = []
        for product in products:
            for category in product.get("categories", []):
                if category.get("slug") == category_slug:
                    category_products.append(product)
                    break
        
        return category_products
    
    def get_low_stock_products(self, threshold: int = 5) -> List[Dict]:
        """Obține produse cu stoc scăzut"""
        products = self.sync_products()
        
        low_stock = []
        for product in products:
            if product.get("manage_stock"):
                stock_qty = product.get("stock_quantity", 0)
                if 0 < stock_qty <= threshold:
                    low_stock.append({
                        "id": product.get("id"),
                        "name": product.get("name"),
                        "sku": product.get("sku"),
                        "stock_quantity": stock_qty,
                        "price": product.get("price")
                    })
        
        return low_stock
    
    def get_out_of_stock_products(self) -> List[Dict]:
        """Obține produse fără stoc"""
        products = self.sync_products()
        
        out_of_stock = []
        for product in products:
            if product.get("stock_status") == "outofstock":
                out_of_stock.append({
                    "id": product.get("id"),
                    "name": product.get("name"),
                    "sku": product.get("sku"),
                    "categories": [cat.get("name") for cat in product.get("categories", [])]
                })
        
        return out_of_stock
    
    def get_recent_orders(self, limit: int = 50) -> List[Dict]:
        """Obține comenzile recente"""
        if not self.is_connected():
            return []
        
        try:
            response = self.api.get("orders", params={
                "per_page": limit,
                "orderby": "date",
                "order": "desc"
            })
            return response.json()
        except Exception as e:
            logger.error(f"Eroare obținere comenzi: {e}")
            return []
    
    def get_sales_stats(self, days: int = 30) -> Dict:
        """Obține statistici vânzări pentru ultimele X zile"""
        if not self.is_connected():
            return {}
        
        try:
            from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            response = self.api.get("reports/sales", params={
                "date_min": from_date,
                "period": "day"
            })
            
            return response.json()
        except Exception as e:
            logger.error(f"Eroare obținere statistici: {e}")
            return {}
    
    def search_products(self, query: str) -> List[Dict]:
        """Caută produse după nume sau descriere"""
        if not self.is_connected():
            return []
        
        try:
            response = self.api.get("products", params={
                "search": query,
                "per_page": 20
            })
            return response.json()
        except KeyboardInterrupt:
            raise  # Permite anularea manuală
        except Exception as e:
            logger.error(f"Eroare căutare produse: {e}")
            return []
    
    def get_product_details_formatted(self, product_id: int = None, sku: str = None) -> str:
        """
        Obține detalii produse formatate pentru agenți
        
        Returns:
            String formatat cu toate detaliile produsului
        """
        product = None
        
        if sku:
            product = self.get_product_by_sku(sku)
        elif product_id:
            product = self.get_product_by_id(product_id)
        
        if not product:
            return "Produs nu a fost găsit."
        
        details = f"""
📦 **{product.get('name', 'N/A')}**

**SKU:** {product.get('sku', 'N/A')}
**Preț:** {product.get('price', '0')} RON
**Preț Regular:** {product.get('regular_price', 'N/A')} RON
**Stoc:** {product.get('stock_quantity', 'N/A')} bucăți
**Status:** {'✅ În stoc' if product.get('stock_status') == 'instock' else '❌ Fără stoc'}

**Categorii:** {', '.join([cat.get('name', '') for cat in product.get('categories', [])])}
**Tags:** {', '.join([tag.get('name', '') for tag in product.get('tags', [])])}

**Descriere:**
{product.get('short_description', product.get('description', 'N/A'))[:500]}...

**Link:** {product.get('permalink', 'N/A')}
"""
        return details.strip()
    
    def get_products_summary(self) -> str:
        """Generează un rezumat al tuturor produselor pentru training agenți"""
        products = self.sync_products()
        
        if not products:
            return "Nu am putut obține lista de produse."
        
        summary_lines = [
            f"📊 **Total Produse:** {len(products)}",
            "",
            "### Produse Disponibile:",
            ""
        ]
        
        for product in products[:100]:  # Limitează la primele 100
            stock_status = "✅" if product.get('stock_status') == 'instock' else "❌"
            stock_qty = product.get('stock_quantity', 'N/A')
            
            summary_lines.append(
                f"{stock_status} **{product.get('name')}** - SKU: {product.get('sku', 'N/A')} | "
                f"Preț: {product.get('price', '0')} RON | Stoc: {stock_qty}"
            )
        
        return "\n".join(summary_lines)
    
    def get_categories_list(self) -> List[Dict]:
        """Obține lista de categorii"""
        if not self.is_connected():
            return []
        
        try:
            response = self.api.get("products/categories", params={"per_page": 100})
            return response.json()
        except Exception as e:
            logger.error(f"Eroare obținere categorii: {e}")
            return []


# Singleton instance
_wc_service = None

def get_woocommerce_service() -> WooCommerceService:
    """Obține instanța singleton a serviciului WooCommerce"""
    global _wc_service
    if _wc_service is None:
        _wc_service = WooCommerceService()
    return _wc_service
