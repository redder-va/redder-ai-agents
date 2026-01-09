from langchain_openai import ChatOpenAI
from memory.vector_store import get_vector_store
from agents.llm_helper import generate_text
from services.woocommerce_service import get_woocommerce_service
import os
import pandas as pd
from io import StringIO

class SalesAnalystAgent:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.llm = None  # Use generate_text fallback
        self.role = 'Agent Analiză Vânzări'
        self.goal = 'Analizează datele de vânzări în timp real de pe redder.ro și face predicții'
        self.backstory = 'Ești un analist bazat pe date pentru Redder.ro, care folosește istoricul vânzărilor din magazin pentru a prezice tendințele și a oferi perspective bazate pe date reale.'
        # Serviciu WooCommerce centralizat
        self.wc = get_woocommerce_service()

    def analyze_sales_data(self, data_path=None):
        """Analizează vânzările reale de pe redder.ro"""
        try:
            # Obține comenzi recente de pe redder.ro
            orders = self.wc.get_recent_orders(limit=100)
            
            if not orders:
                return "**Nu am putut obține date despre comenzi de pe redder.ro.**"
            
            # Procesează datele în DataFrame
            sales_data = []
            total_revenue = 0
            
            for order in orders:
                order_total = float(order.get('total', 0))
                total_revenue += order_total
                
                for item in order.get('line_items', []):
                    sales_data.append({
                        'product': item['name'],
                        'quantity': item['quantity'],
                        'total': float(item['total']),
                        'date': order['date_created'][:10],  # Doar data
                        'status': order['status']
                    })
            
            if not sales_data:
                return "**Nu există date de vânzări.**"
            
            df = pd.DataFrame(sales_data)
            
            # Rezumat pe produse
            summary_df = df.groupby('product').agg({
                'quantity': 'sum',
                'total': 'sum'
            }).reset_index().sort_values('total', ascending=False)
            
            summary_df.columns = ['Produs', 'Cantitate', 'Total Vânzări (RON)']
            summary_df['Total Vânzări (RON)'] = summary_df['Total Vânzări (RON)'].round(2)
            
            # Creare output Markdown
            markdown_output = "# 📊 Raport Analiză Vânzări Redder.ro\n\n"
            markdown_output += f"**Perioada:** Ultimele {len(orders)} comenzi\n"
            markdown_output += f"**Total comenzi analizate:** {len(orders)}\n"
            markdown_output += f"**Venit total:** {total_revenue:.2f} RON\n\n"
            
            # Status comenzi
            status_counts = df['status'].value_counts()
            markdown_output += "## Status Comenzi\n\n"
            for status, count in status_counts.items():
                icon = "✅" if status == "completed" else "🕒" if status == "processing" else "⚠️"
                markdown_output += f"- {icon} **{status}:** {count} comenzi\n"
            
            markdown_output += "\n## Top 20 Produse Vândute\n\n"
            markdown_output += summary_df.head(20).to_markdown(index=False)
            
            markdown_output += f"\n\n**Total general:** {summary_df['Total Vânzări (RON)'].sum():.2f} RON"
            markdown_output += f"\n**Produse unice:** {len(summary_df)} produse"
            
            return markdown_output
            
        except Exception as e:
            return f"**❌ Eroare la preluarea datelor de pe redder.ro:** {e}"

    def predict_sales(self, current_data):
        sales_summary = self.analyze_sales_data()
        knowledge = "\n".join([doc.page_content for doc in self.vector_store.similarity_search(current_data, k=3)])
        prompt = f"Tu ești {self.role}. {self.backstory}. Obiectivul tău este: {self.goal}. Rezumat vânzări: {sales_summary}. Date anterioare: {knowledge}. Pe baza acestor date, prezice vânzările viitoare În ROMÂNĂ: {current_data}"
        prediction = generate_text(self.llm, prompt)
        self.vector_store.add_texts([f"Predicție: {prediction}"])
        return prediction