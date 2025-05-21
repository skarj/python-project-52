import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

logger = logging.getLogger(__name__)


class LoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request,
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
        return redirect(reverse('login'))


class OwnershipRequiredMixin(UserPassesTestMixin):
    model = None
    success_url = None
    permission_denied_message = "У вас нет прав для выполнения этого действия."
    redirect_url_name = None

    def test_func(self):
        obj = self.get_object()
        return self.request.user == getattr(obj, 'author', obj)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.redirect_url_name or self.success_url)


class ProtectedDeleteMixin:
    protected_error_message = "Невозможно удалить объект, так как он связан с другими объектами."  # noqa E501

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except ProtectedError:
            messages.error(request, self.protected_error_message)
            logger.exception(f"ProtectedError when deleting object {self.get_object().id}")  # noqa E501
            return HttpResponseRedirect(self.success_url)
