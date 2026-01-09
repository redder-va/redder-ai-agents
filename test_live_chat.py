"""
Test pentru LiveChatAgent cu date reale din WooCommerce
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents.live_chat import LiveChatAgent

def test_chat():
    """Test conversații cu agentul de chat"""
    agent = LiveChatAgent()
    
    print("=" * 60)
    print("TEST LIVECHAT AGENT - Date Reale din redder.ro")
    print("=" * 60)
    
    # Test 1: Salut simplu
    print("\n1️⃣ TEST: Salut inițial")
    print("-" * 60)
    result1 = agent.chat("Bună! Ce produse aveți?")
    print(f"RĂSPUNS:\n{result1['response']}\n")
    if result1.get('suggested_products'):
        print("PRODUSE SUGERATE:")
        for p in result1['suggested_products']:
            print(f"  - {p['name']} | {p['price']} RON | {p['stock_status']}")
    print(f"QUICK REPLIES: {result1.get('quick_replies', [])}")
    
    # Test 2: Comparație vodcă
    print("\n\n2️⃣ TEST: Comparație între vodka")
    print("-" * 60)
    result2 = agent.chat("Care este diferența între Kumaniok și Valahia Gold?")
    print(f"RĂSPUNS:\n{result2['response']}\n")
    if result2.get('suggested_products'):
        print("PRODUSE SUGERATE:")
        for p in result2['suggested_products']:
            print(f"  - {p['name']} | {p['price']} RON | {p['stock_status']}")
    
    # Test 3: Rețetă cocktail
    print("\n\n3️⃣ TEST: Cerere rețetă cocktail")
    print("-" * 60)
    result3 = agent.chat("Cum pot face un Moscow Mule?")
    print(f"RĂSPUNS:\n{result3['response']}\n")
    if result3.get('suggested_products'):
        print("PRODUSE SUGERATE:")
        for p in result3['suggested_products']:
            print(f"  - {p['name']} | {p['price']} RON | Link: {p['link']}")
    
    # Test 4: Stocuri
    print("\n\n4️⃣ TEST: Verificare stoc produse")
    print("-" * 60)
    result4 = agent.chat("Aveți în stoc ORO del Sole Peach?")
    print(f"RĂSPUNS:\n{result4['response']}\n")
    
    # Test 5: Conversație cu istoric
    print("\n\n5️⃣ TEST: Conversație cu istoric")
    print("-" * 60)
    history = [
        {'role': 'user', 'content': 'Vreau o vodcă bună'},
        {'role': 'assistant', 'content': 'Recomand Valahia Gold 40% sau Kumaniok 38%'}
    ]
    result5 = agent.chat("Care e diferența de preț?", conversation_history=history)
    print(f"RĂSPUNS:\n{result5['response']}\n")
    
    print("\n" + "=" * 60)
    print("TEST FINALIZAT!")
    print("=" * 60)

if __name__ == "__main__":
    test_chat()
