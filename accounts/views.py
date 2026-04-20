from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile
from .forms import ProfileUpdateForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "accounts/profile_form.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy(
            "accounts:profile_update", kwargs={"username": self.request.user.username}
        )


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")

def permission_denied_view(request):
    return render(request, "accounts/permission_denied.html")
