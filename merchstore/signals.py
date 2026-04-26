from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction as db_transaction
from .models import Transaction


@receiver(post_save, sender=Transaction)
def update_product_stock(sender, instance, created, **kwargs):
    if not created:
        return

    product = instance.product

    product.stock = max(0, product.stock - instance.amount)

    if product.stock == 0:
        product.status = "OUT_OF_STOCK"
    else:
        product.status = "AVAILABLE"
        
    product.save()


        
        

