from django.contrib import admin
from .models import Product, ProductType, Transaction


class ProductInline(admin.TabularInline):
    model = Product


class TransactionInline(admin.TabularInline):
    model = Transaction


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    inlines = [
        ProductInline,
    ]

    list_display = ("name", "description")
    search_fields = ("name",)

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

    list_display = (
        "name",
        "price",
        "product_type",
        "stock",
        "status",
        "owner",
    )
    search_fields = ("name", "description")
    list_filter = ("product_type", "price")

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": ("name", "product_type", "owner"),
            },
        ),
        (
            "Product Details",
            {
                "fields": ("description", "product_image"),
            },
        ),
        (
            "Inventory",
            {
                "fields": ("price", "stock", "status"),
            },
        ),
    )


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "buyer",
        "product",
        "amount",
        "status",
        "created_on",
    )
    list_filter = ("status", "created_on")
    search_fields = (
        "buyer__user__username",
        "product__name",
    )


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
