from django.contrib import admin
from .models import Product, ProductType


class ProductInline(admin.TabularInline):
    model = Product


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    inlines = [ProductInline, ]

admin.site.register(ProductType, ProductTypeAdmin)