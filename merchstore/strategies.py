from django.shortcuts import redirect
from django.contrib import messages


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

        messages.success(request, product.name, extra_tags="product_added_to_cart")

        return redirect("merchstore:cart")


class GuestPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        request.session["pending_transaction"] = {
            "product_id": product.id,
            "amount": form.cleaned_data["amount"],
        }

        messages.info(
            request,
            "Please log in to continue your purchase",
            extra_tags="merch_login_required",
        )

        return redirect("accounts:login")
