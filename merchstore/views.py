from django.shortcuts import (
    render, 
    redirect, 
    get_object_or_404
)
from django.urls import reverse_lazy
from collections import defaultdict
from django.views.generic import (
    ListView,
    DetailView,
    CreateView, 
    UpdateView, 
    TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TransactionForm, ProductCreateUpdateForm
from .models import Product, Transaction
from accounts.mixins import RoleRequiredMixin
from .strategies import (
    AuthenticatedPurchaseStrategy, 
    GuestPurchaseStrategy
)


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "product_list.html"

    def get_queryset(self):
        queryset = Product.objects.all()
            # Excludes user's own products from "all products"
        if self.request.user.is_authenticated:   
            queryset = queryset.exclude(owner=self.request.user.profile)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user_products = Product.objects.filter(owner=self.request.user.profile)
            context['user_products'] = user_products
        else:
            context['user_products'] = []
        
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "product_detail.html"

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = TransactionForm()
        
        is_owner = (
            request.user.is_authenticated
            and 
            request.user.profile == product.owner
        )
        can_buy = (
            request.user.is_authenticated
            and
            not is_owner
            and 
            product.stock > 0
        )
        
        return render(request, self.template_name, {
            'product': product,
            'form': form,
            'is_owner': is_owner,
            'can_buy': can_buy,
        })

    def post(self, request, pk):
        product =get_object_or_404(Product, pk=pk)
        form = TransactionForm(request.POST)

        if form.is_valid():
            # Chose strat. based on authentication
            if request.user.is_authenticated:
                strategy = AuthenticatedPurchaseStrategy()
            else:
                strategy = GuestPurchaseStrategy()
            return strategy.execute(request, product, form)

        is_owner = (
            request.user.is_authenticated
            and 
            request.user.profile == product.owner
        )
        can_buy = (
            request.user.is_authenticated
            and
            not is_owner
            and 
            product.stock > 0
        )

        return render(request, self.template_name, {
            'product': product,
            'form': form,
            'is_owner': False,
            'can_buy': product.stock > 0
        })       
       

class ProductCreateView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateUpdateForm
    template_name = "product_create.html"
    required_role = "Market Seller"
    
    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'merchstore:product_detail', 
            kwargs={'pk': self.object.pk}
        )


class ProductUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductCreateUpdateForm
    template_name = "product_update.html"
    required_role = "Market Seller"
    
    def form_valid(self, form):
        form.instance.owner = self.object.owner

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'merchstore:product_detail', 
            kwargs={'pk': self.object.pk}
        )


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile

        transactions = Transaction.objects.filter(
            buyer=user_profile
        ).select_related('product', 'product__owner')

        cart_by_owner = defaultdict(list)
        for t in transactions:
            cart_by_owner[t.product.owner].append(t)

        context['cart_by_owner'] = dict(cart_by_owner)
        return context


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = "transactions"
    template_name = "transaction_list.html"
    
    def get_queryset(self):
        # Transactions where logged-in user is the seller
        return Transaction.objects.filter(
            product__owner=self.request.user.profile
        ).select_related("buyer", "product")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped_transactions = defaultdict(list)

        for t in context["transactions"]:
            grouped_transactions[t.buyer].append(t)

        context["grouped_transactions"] = dict(grouped_transactions)
        return context

