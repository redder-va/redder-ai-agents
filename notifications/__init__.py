"""
Modul de notificări pentru Redder.ro AI Agents
Conține funcționalități pentru trimiterea de notificări prin diverse canale
"""

from .telegram_notifier import get_telegram_notifier, TelegramNotifier

__all__ = ['get_telegram_notifier', 'TelegramNotifier']
