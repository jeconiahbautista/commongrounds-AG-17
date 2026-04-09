from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "product_list.html"

    def get_queryset(self):
        queryset = Product.objects.all()

        if self.request.user.is_authenticated:   
            queryset = queryset.exclude(owner=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user_products = Product.objects.filter(owner=self.request.user)
            context['user_products'] = user_products
          
        else:
            context['user_products'] = []

        return context

class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "product_detail.html"


class ProductCreateView


class ProductUpdateView


class CartView


class TransactionListView