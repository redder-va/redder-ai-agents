"""
Services Package
Servicii centralizate pentru integrări externe
"""

from .woocommerce_service import get_woocommerce_service, WooCommerceService

__all__ = ['get_woocommerce_service', 'WooCommerceService']
