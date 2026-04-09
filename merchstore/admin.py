from django.contrib import admin
from .models import Product, ProductType


class ProductInline(admin.TabularInline):
    model = Product


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    inlines = [
        ProductInline,
    ]

    fieldsets = [
        (
            "Details",
            {
                "fields": [
                    ("name", "description"),
                ]
            },
        )
    ]


class ProductAdmin(admin.ModelAdmin):
    model = Product
    search_fields = ("name",)
    list_display = (
        "name",
        "price",
        "product_type",
    )
    list_filter = ("product_type", "price")
    fieldsets = [
        (
            "Details",
            {
                "fields": [
                    ("name", "product_type", "price"),
                    "description",
                ]
            },
        )
    ]


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
