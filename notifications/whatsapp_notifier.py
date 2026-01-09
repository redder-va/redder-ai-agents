"""
Modul pentru trimitere notificări WhatsApp prin Twilio
"""
import os
from datetime import datetime
from twilio.rest import Client

class WhatsAppNotifier:
    def __init__(self):
        """
        Inițializează clientul Twilio pentru WhatsApp
        Necesită variabile de mediu:
        - TWILIO_ACCOUNT_SID
        - TWILIO_AUTH_TOKEN
        - TWILIO_WHATSAPP_FROM (format: whatsapp:+14155238886)
        """
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_from = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
        self.notification_number = 'whatsapp:+40763038001'  # Numărul hardcodat pentru notificări
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
            print("⚠️ WhatsApp notifications DISABLED - Twilio credentials not configured")

    def send_order_notification(self, order_data):
        """
        Trimite notificare WhatsApp pentru comandă nouă
        
        Args:
            order_data (dict): Dicționar cu datele comenzii
                - order_number: Număr comandă
                - customer_name: Nume client
                - customer_phone: Telefon client
                - customer_email: Email client
                - items: Lista de produse (listă de dict cu 'name', 'quantity', 'price')
                - total: Total comandă
                - payment_method: Metodă de plată
                - shipping_address: Adresă livrare
                - notes: Notițe comandă (opțional)
        
        Returns:
            bool: True dacă trimiterea a avut succes, False altfel
        """
        if not self.enabled:
            print("❌ WhatsApp notification NOT sent - Twilio not configured")
            return False
        
        try:
            message = self._format_order_message(order_data)
            
            result = self.client.messages.create(
                from_=self.whatsapp_from,
                body=message,
                to=self.notification_number
            )
            
            print(f"✅ WhatsApp notification sent! SID: {result.sid}")
            return True
            
        except Exception as e:
            print(f"❌ WhatsApp notification FAILED: {str(e)}")
            return False

    def _format_order_message(self, order_data):
        """
        Formatează mesajul WhatsApp pentru notificare comandă
        """
        # Header
        message = f"🛍️ *COMANDĂ NOUĂ REDDER.RO*\n"
        message += f"{'='*40}\n\n"
        
        # Detalii comandă
        message += f"📋 *Comandă:* #{order_data.get('order_number', 'N/A')}\n"
        message += f"📅 *Data:* {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
        
        # Detalii client
        message += f"👤 *CLIENT*\n"
        message += f"Nume: {order_data.get('customer_name', 'N/A')}\n"
        message += f"Telefon: {order_data.get('customer_phone', 'N/A')}\n"
        message += f"Email: {order_data.get('customer_email', 'N/A')}\n\n"
        
        # Produse
        message += f"📦 *PRODUSE*\n"
        items = order_data.get('items', [])
        for item in items:
            name = item.get('name', 'Produs')
            qty = item.get('quantity', 1)
            price = item.get('price', 0)
            subtotal = qty * price
            message += f"• {name}\n"
            message += f"  {qty} x {price:.2f} RON = {subtotal:.2f} RON\n"
        
        message += "\n"
        
        # Total
        total = order_data.get('total', 0)
        message += f"💰 *TOTAL: {total:.2f} RON*\n\n"
        
        # Metodă plată
        payment = order_data.get('payment_method', 'N/A')
        message += f"💳 *Plată:* {payment}\n\n"
        
        # Adresă livrare
        address = order_data.get('shipping_address', 'N/A')
        message += f"🚚 *Livrare:*\n{address}\n\n"
        
        # Notițe (dacă există)
        notes = order_data.get('notes', '')
        if notes:
            message += f"📝 *Notițe:*\n{notes}\n\n"
        
        # Footer
        message += f"{'='*40}\n"
        message += f"🔗 Acces panou: https://redder.ro/wp-admin"
        
        return message

    def send_custom_message(self, message_text):
        """
        Trimite un mesaj personalizat pe WhatsApp
        
        Args:
            message_text (str): Textul mesajului
        
        Returns:
            bool: True dacă trimiterea a avut succes, False altfel
        """
        if not self.enabled:
            print("❌ WhatsApp message NOT sent - Twilio not configured")
            return False
        
        try:
            result = self.client.messages.create(
                from_=self.whatsapp_from,
                body=message_text,
                to=self.notification_number
            )
            
            print(f"✅ WhatsApp message sent! SID: {result.sid}")
            return True
            
        except Exception as e:
            print(f"❌ WhatsApp message FAILED: {str(e)}")
            return False

# Singleton instance
_whatsapp_notifier = None

def get_whatsapp_notifier():
    """Returnează instanța singleton a WhatsAppNotifier"""
    global _whatsapp_notifier
    if _whatsapp_notifier is None:
        _whatsapp_notifier = WhatsAppNotifier()
    return _whatsapp_notifier
