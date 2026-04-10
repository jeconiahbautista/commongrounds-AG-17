from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import Http404

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView, TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TransactionForm, ProductCreateUpdateForm
from .models import Product, Transaction


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

    def get(self, request, pk):
        try:
            product = Product.object.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")
        
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
        try:
            product = Product.object.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")
        
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.profile == product.owner:
            return redirect('merchstore:product_detail', pk=pk)

        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.product = product
            transaction.buyer = request.user.profile

            if transaction.amount > product.stock:
                form.add_error('amount', "Only {} item(s) in stock.".format(product.stock)  )
            else:
                product.stock -= transaction.amount
                product.save()
                transaction.save()
                return redirect('merchstore:cart')
        
        return render(request, self.template_name, {
            'product': product,
            'form': form,
            'is_owner': False,
            'can_buy': product.stock > 0,
        })

#Market seller not yet included
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateUpdateForm
    template_name = "product_create.html"
    
    def get_success_url(self):
        return reverse_lazy(
            'merchstore:product_detail', 
            kwargs={'pk': self.object.pk}
        )
    
    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductCreateUpdateForm
    template_name = "product_update.html"

    def get_success_url(self):
        return reverse_lazy(
            'merchstore:product_detail', 
            kwargs={'pk': self.object.pk}
        )
    
    def form_valid(self, form):
        form.instance.owner = self.object.owner

        if form.instance.stock == 0:
            form.instance.status = 'OUT_OF_STOCK'
        else:
            form.instance.status = 'AVAILABLE'

        return super().form_valid(form)


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile

        transactions = Transaction.objects.filter(
            buyer=user_profile
        ).select_related('product', 'product__owner')

        cart_by_owner = {}
        for i in transactions:
            owner = i.product.owner
            if owner not in cart_by_owner:
                cart_by_owner[owner] = []
            cart_by_owner[owner].append(i)

        context['cart_by_owner'] = cart_by_owner
        return context


#class TransactionListView