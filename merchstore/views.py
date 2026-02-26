from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product

def index(request):
    return HttpResponse('Welcome to the Merchandise Store.')

class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product_list.html'

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'
