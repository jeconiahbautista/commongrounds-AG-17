from django import forms
from .models import Profile
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordResetForm,
)
from django.contrib.auth.models import User


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name"]


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "login-field",
                "placeholder": "Enter a valid username",
            }
        )
    )
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "login-field",
            }
        ),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "login-field",
                "placeholder": "Enter a password with at least 8 characters.",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "login-field",
                "placeholder": "Re-enter your password",
            }
        )
    )

    class Meta:
        model = User
        fields = ["username", "role", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=commit)

        Profile.objects.create(
            user=user,
            display_name=user.username,
            email_address=user.email,
            role=self.cleaned_data["role"],
        )

        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "login-field",
                "placeholder": "Enter your username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "login-field",
                "placeholder": "Enter your password",
            }
        )
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "login-field",
                "placeholder": "Enter your email",
            }
        )
    )
