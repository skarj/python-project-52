from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from task_manager.users.models import User


class LoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, "Вы не авторизованы! Пожалуйста, выполните вход."
            )
            return redirect(self.get_login_url())

        return super().dispatch(request, *args, **kwargs)


class UserModificationMixin(UserPassesTestMixin):
    model = User
    success_url = reverse_lazy('users_index')

    def test_func(self) -> bool:
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(
            self.request, "У вас нет прав для изменения другого пользователя."
        )
        return redirect('users_index')
