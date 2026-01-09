#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script automat de antrenare agenți
Rulează zilnic pentru a actualiza cunoștințele agenților cu produsele de pe Redder.ro
"""

import sys
import os

# Adaugă directorul părinte în path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper.product_scraper import ProductScraper
from scraper.agent_trainer import AgentTrainer
from datetime import datetime

def main():
    """Proces complet de scraping și training"""
    
    print("=" * 70)
    print("🤖 SISTEM AUTOMAT DE ANTRENARE AGENȚI AI - REDDER.RO")
    print("=" * 70)
    print(f"\n📅 Data: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
    
    # PASUL 1: Extrage produse de pe site
    print("\n" + "─" * 70)
    print("📡 PASUL 1: EXTRAGERE PRODUSE DE PE REDDER.RO")
    print("─" * 70 + "\n")
    
    scraper = ProductScraper()
    scraper_success = scraper.run()
    
    if not scraper_success:
        print("\n❌ Scraping-ul a eșuat. Training anulat.")
        return False
    
    # PASUL 2: Antrenează agenții cu produsele extrase
    print("\n" + "─" * 70)
    print("🎓 PASUL 2: ANTRENARE AGENȚI CU PRODUSELE EXTRASE")
    print("─" * 70 + "\n")
    
    trainer = AgentTrainer()
    training_success = trainer.run(test=True)
    
    if not training_success:
        print("\n❌ Training-ul a eșuat.")
        return False
    
    # SUCCES
    print("\n" + "=" * 70)
    print("✅ ANTRENARE COMPLETĂ FINALIZATĂ CU SUCCES!")
    print("=" * 70)
    print("\n🎉 Agenții tăi AI sunt acum experți în produsele Redder.ro!")
    print("\n💡 NEXT STEPS:")
    print("   1. Testează agenții în dashboard (http://localhost:3000)")
    print("   2. Întreabă despre orice produs de pe site")
    print("   3. Agenții vor răspunde cu informații actualizate")
    print("\n📅 Recomandare: Rulează acest script zilnic pentru produse fresh!")
    print("   Poți automatiza cu Windows Task Scheduler sau cron job")
    
    return True


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Training oprit de utilizator.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ EROARE CRITICĂ: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
