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
        widgets = {
            'amount': forms.NumberInput(attrs={
                'placeholder': 'Enter amount',
                'class': 'buy-input'
            })
        }
    

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
            'name': forms.TextInput(attrs={
                'placeholder':'Enter Product Name'
            }),
            'description': forms.TextInput(attrs={
                'placeholder':'Enter Product Description'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder':'Enter Price'
            }),
            'stock': forms.NumberInput(attrs={
                'placeholder': 'Enter amount',
                'class': 'buy-input'
            }),
            'status': forms.Select(),
            'product_type': forms.Select()
        }
 