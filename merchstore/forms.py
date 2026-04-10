from django import forms
from .models import (
    Transaction,
    Product,
    ProductType,
)

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
    

class ProductCreateUpdateForm(forms.ModelForm):

    product_type = forms.ModelChoiceField(
        queryset=ProductType.objects.all(),
        widget=forms.Select(),
        required=True
    )
    class Meta:
        model = Product
        fields = [
            'name', 
            'product_type', 
            'description', 
            'price', 
            'stock', 
            'status', 
            'product_image'
        ]
        widgets = {
            'product_type': forms.Select(),
            'status': forms.Select()
        }
