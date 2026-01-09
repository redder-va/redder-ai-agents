"""
Test script pentru Link Generator
"""

from agents.link_generator import get_link_generator

def test_link_generator():
    print("=== TEST LINK GENERATOR ===\n")
    
    link_gen = get_link_generator()
    
    # Test 1: Link simplu pentru campanie
    print("1. Link campanie vodka:")
    link1 = link_gen.generate_campaign_link("vodka", "promotie-iarna", "email", "cumpara")
    print(f"   {link1}\n")
    
    # Test 2: Link pentru categorie generală
    print("2. Link magazin general:")
    link2 = link_gen.generate_campaign_link("magazin", "black-friday", "social", "descopera")
    print(f"   {link2}\n")
    
    # Test 3: CTA Button
    print("3. CTA Button Markdown:")
    button = link_gen.get_cta_button("🛒 Cumpără Vodka Premium", "vodka", "premium-vodka", "email")
    print(f"   {button}\n")
    
    # Test 4: Linkuri pentru toate categoriile
    print("4. Linkuri categorii în Markdown:")
    categories = link_gen.get_category_links_markdown("campanie-test", "newsletter")
    print(categories)
    
    # Test 5: Injectare linkuri în text campanie
    print("\n5. Campanie cu linkuri injectate:")
    sample_campaign = """
## Promoție Specială Vodka
    
Descoperă cele mai fine vodka premium la prețuri speciale!

### Oferte:
- Vodka Premium 40% - 89 RON
- Set 3 Vodka Artizanale - 199 RON

Comandă acum și primești livrare gratuită!
"""
    
    campaign_with_links = link_gen.inject_links_in_campaign(sample_campaign, "promotie-vodka", "email")
    print(campaign_with_links)

if __name__ == "__main__":
    test_link_generator()
