"""
Modul de notificări pentru Redder.ro AI Agents
Conține funcționalități pentru trimiterea de notificări prin diverse canale
"""

from .whatsapp_notifier import get_whatsapp_notifier, WhatsAppNotifier

__all__ = ['get_whatsapp_notifier', 'WhatsAppNotifier']
