from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile
from .forms import ProfileUpdateForm, CustomLoginForm, CustomUserCreationForm, CustomPasswordResetForm
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth import login


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "profile_form.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy(
            "accounts:profile_update", kwargs={"username": self.request.user.username}
        )


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "registration/login.html"


class CustomResetPasswordView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "registration/password_reset_form.html"


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


def permission_denied_view(request):
    return render(request, "permission_denied.html")
