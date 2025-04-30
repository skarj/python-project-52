from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class LoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, "Вы не авторизованы! Пожалуйста, выполните вход."
            )
            return redirect(self.get_login_url())

        return super().dispatch(request, *args, **kwargs)
