import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from task_manager.users.models import User

logger = logging.getLogger(__name__)


class LoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request,
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
        return redirect(reverse('login'))


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


class TaskDeletekMixin:
    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(self.request, "Задачу может удалить только ее автор")
        return redirect("tasks_index")


class ProtectedDeleteMixin:
    protected_error_message = "Невозможно удалить объект, так как он связан с другими объектами."  # noqa E501
    success_message = "Объект успешно удален"

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, self.success_message)
            return response
        except ProtectedError as e:
            messages.error(request, self.protected_error_message)
            logger.exception(f"ProtectedError when deleting object {self.get_object().id}: {e}")  # noqa E501
            return HttpResponseRedirect(self.success_url)
