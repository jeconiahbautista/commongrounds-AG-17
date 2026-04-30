from django.db import models
from django.urls import reverse

from accounts.models import Profile
from django.core.validators import MinValueValidator


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType, 
        null=True,
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name="products"
    )
    owner = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name="products",
        null=True,
        blank=True 
    )
    product_image = models.ImageField(
        upload_to='product_images/', 
        null=True, 
        blank=True
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    stock = models.PositiveIntegerField()
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('ON_SALE', 'On sale'),
        ('OUT_OF_STOCK', 'Out of stock'),
    ]
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='AVAILABLE',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "merchstore:product_detail", 
            args=[str(self.id)]
        )

    class Meta:
        ordering = ["name"]


class Transaction(models.Model):
    buyer = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buyer_transactions'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.PositiveIntegerField()
    STATUS_CHOICES = [
        ('ON_CART', 'On cart'),
        ('TO_PAY', 'To Pay'),
        ('TO_SHIP', 'To Ship'),
        ('TO_RECEIVE', 'To Receive'),
        ('DELIVERED', 'Delivered'),
    ]
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='ON_CART',
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {} at {}".format(
            self.buyer,
            self.product,
            self.amount
        )

    class Meta:
        ordering = ['created_on']

    
