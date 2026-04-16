from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class RoleRequiredMixin(AccessMixin):
    required_role = None
    permission_denied_url = "accounts:permission_denied"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if self.required_role is None:
            raise ValueError("RoleRequiredMixin requires 'required_role' to be set.")

        user_profile = getattr(request.user, "profile", None)
        if user_profile is None or user_profile.role != self.required_role:
            return redirect(self.permission_denied_url)

        return super().dispatch(request, *args, **kwargs)
