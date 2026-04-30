from django.shortcuts import redirect


class BaseTransactionStrategy:

    def execute(self, request, product, form):
        raise NotImplementedError("Subclasses must implement this method")


class AuthenticatedPurchaseStrategy(BaseTransactionStrategy):
    
    def execute(self, request, product, form):
        transaction = form.save(commit=False)
        transaction.product = product
        transaction.buyer = request.user.profile
        transaction.status = "ON_CART"
        transaction.save()

        return redirect('merchstore:cart')
    
class GuestPurchaseStrategy(BaseTransactionStrategy):

    def execute(self, request, product, form):
        request.session['pending_transaction'] = {
            'product_id' : product.id,
            'amount' : form.cleaned_data['amount'],
        }

        return redirect('accounts:login')