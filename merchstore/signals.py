from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction as db_transaction
from .models import Transaction


@receiver(post_save, sender=Transaction)
def update_product_stock(sender, instance, created, **kwargs):
    if not created:
        return

    product = instance.product

    with db_transaction.atomic():
        product.stock -= instance.amount

        if product.stock <= 0:
            product.stock = 0
            product.status = "OUT_OF_STOCK"
        else:
            if product.status == "OUT_OF_STOCK":
                product.status = "AVAILABLE"

        product.save()

        
        

