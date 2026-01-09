"""
Modul pentru trimitere notificări Telegram
100% gratuit, fără limite
"""
import os
import requests
from datetime import datetime

class TelegramNotifier:
    def __init__(self):
        """
        Inițializează clientul Telegram
        Necesită variabile de mediu:
        - TELEGRAM_BOT_TOKEN
        - TELEGRAM_CHAT_ID
        """
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if self.bot_token and self.chat_id:
            self.enabled = True
            self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        else:
            self.enabled = False
            print("⚠️ Telegram notifications DISABLED - credentials not configured")

    def send_message(self, text):
        """
        Trimite mesaj simplu pe Telegram
        
        Args:
            text (str): Textul mesajului
        
        Returns:
            bool: True dacă trimiterea a avut succes, False altfel
        """
        if not self.enabled:
            print("❌ Telegram notification NOT sent - not configured")
            return False
        
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                print("✅ Telegram notification sent successfully")
                return True
            else:
                print(f"❌ Telegram error: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Telegram exception: {e}")
            return False

    def send_order_notification(self, order_data):
        """
        Trimite notificare pentru comandă nouă
        
        Args:
            order_data (dict): Dicționar cu datele comenzii
                - order_number: Număr comandă
                - customer_name: Nume client
                - customer_phone: Telefon client
                - customer_email: Email client
                - items: Lista de produse
                - total: Total comandă
                - payment_method: Metodă de plată
                - shipping_address: Adresă livrare
        
        Returns:
            bool: True dacă trimiterea a avut succes
        """
        try:
            # Construiește mesaj formatat
            message = f"""
🛒 <b>COMANDĂ NOUĂ #{order_data.get('order_number', 'N/A')}</b>

👤 <b>Client:</b> {order_data.get('customer_name', 'N/A')}
📱 <b>Telefon:</b> {order_data.get('customer_phone', 'N/A')}
📧 <b>Email:</b> {order_data.get('customer_email', 'N/A')}

📦 <b>Produse:</b>
"""
            
            # Adaugă produse
            items = order_data.get('items', [])
            if items:
                for item in items:
                    name = item.get('name', 'Produs')
                    qty = item.get('quantity', 1)
                    price = item.get('price', 0)
                    message += f"  • {name} x{qty} - {price} RON\n"
            else:
                message += "  • Detalii indisponibile\n"
            
            # Total și plată
            total = order_data.get('total', 'N/A')
            payment = order_data.get('payment_method', 'N/A')
            message += f"""
💰 <b>Total:</b> {total} RON
💳 <b>Plată:</b> {payment}

📍 <b>Livrare:</b>
{order_data.get('shipping_address', 'Adresă indisponibilă')}
"""
            
            # Notițe (dacă există)
            notes = order_data.get('notes')
            if notes:
                message += f"\n📝 <b>Notițe:</b> {notes}\n"
            
            # Timestamp
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            message += f"\n🕐 {timestamp}"
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"❌ Error building order notification: {e}")
            # Fallback la mesaj simplu
            simple_msg = f"🛒 Comandă nouă #{order_data.get('order_number', 'N/A')} de la {order_data.get('customer_name', 'Client')}"
            return self.send_message(simple_msg)


# Singleton instance
_telegram_notifier = None

def get_telegram_notifier():
    """Returnează instanța singleton a notifier-ului Telegram"""
    global _telegram_notifier
    if _telegram_notifier is None:
        _telegram_notifier = TelegramNotifier()
    return _telegram_notifier
