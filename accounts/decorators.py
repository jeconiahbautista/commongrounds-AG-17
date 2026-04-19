from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            user_profile = getattr(request.user, "profile", None)
            if user_profile is None or user_profile.role != required_role:
                return redirect("accounts:permission_denied")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
