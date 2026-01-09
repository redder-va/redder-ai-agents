"""
Test sincronizare WooCommerce cu redder.ro
Verifică conexiunea și sincronizarea produselor
"""

import os
os.chdir(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from services.woocommerce_service import get_woocommerce_service

def test_woocommerce_connection():
    print("="*60)
    print("TEST CONEXIUNE WOOCOMMERCE - redder.ro")
    print("="*60)
    
    wc = get_woocommerce_service()
    
    # 1. Test conexiune
    print("\n1. Verificare conexiune...")
    if wc.is_connected():
        print("✅ API WooCommerce conectat")
    else:
        print("❌ API WooCommerce NU este conectat")
        print("   Verifică credentials în .env:")
        print("   - WOOCOMMERCE_URL")
        print("   - WOOCOMMERCE_KEY")
        print("   - WOOCOMMERCE_SECRET")
        return
    
    # 2. Test sincronizare produse
    print("\n2. Sincronizare produse de pe redder.ro...")
    products = wc.sync_products(force=True)
    print(f"✅ Sincronizat {len(products)} produse")
    
    if products:
        # Afișează primele 5 produse
        print("\n3. Primele 5 produse:")
        for i, product in enumerate(products[:5], 1):
            stock_qty = product.get('stock_quantity', 'N/A')
            stock_status = "✅" if product.get('stock_status') == 'instock' else "❌"
            print(f"   {i}. {stock_status} {product.get('name')} - {product.get('price', 'N/A')} RON | Stoc: {stock_qty}")
    
    # 4. Test produse cu stoc scăzut
    print("\n4. Produse cu stoc scăzut (sub 5 bucăți):")
    low_stock = wc.get_low_stock_products(threshold=5)
    if low_stock:
        for item in low_stock[:10]:
            print(f"   ⚠️  {item['name']} - Stoc: {item['stock_quantity']} bucăți")
    else:
        print("   ✅ Nu există produse cu stoc scăzut")
    
    # 5. Test produse fără stoc
    print("\n5. Produse fără stoc:")
    out_of_stock = wc.get_out_of_stock_products()
    print(f"   Total produse fără stoc: {len(out_of_stock)}")
    if out_of_stock:
        for item in out_of_stock[:5]:
            print(f"   ❌ {item['name']} (SKU: {item['sku']})")
    
    # 6. Test categorii
    print("\n6. Categorii produse:")
    categories = wc.get_categories_list()
    print(f"   Total categorii: {len(categories)}")
    for cat in categories[:10]:
        print(f"   - {cat.get('name')} ({cat.get('count', 0)} produse)")
    
    # 7. Test căutare produs
    print("\n7. Test căutare produs 'vodka':")
    search_results = wc.search_products("vodka")
    if search_results:
        print(f"   Găsite {len(search_results)} produse:")
        for product in search_results[:3]:
            print(f"   - {product.get('name')} - {product.get('price')} RON")
    
    # 8. Test comenzi recente
    print("\n8. Comenzi recente:")
    orders = wc.get_recent_orders(limit=10)
    if orders:
        print(f"   Total comenzi: {len(orders)}")
        for order in orders[:3]:
            print(f"   - Comandă #{order.get('id')} - {order.get('total')} RON - Status: {order.get('status')}")
    else:
        print("   Nu s-au găsit comenzi")
    
    print("\n" + "="*60)
    print("✅ TEST COMPLET!")
    print("="*60)

if __name__ == "__main__":
    test_woocommerce_connection()
