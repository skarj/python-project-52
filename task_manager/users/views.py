import logging

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.mixins import LoginRequiredMixin, UserModificationMixin
from task_manager.users import forms
from task_manager.users.models import User

logger = logging.getLogger(__name__)


class UserIndex(ListView):
    model = User
    template_name = "users/index.html"


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = forms.UserCreateForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = "Пользователь успешно зарегистрирован"


class UserUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                     UserModificationMixin, UpdateView):
    template_name = "users/update.html"
    form_class = forms.UserCreateForm
    pk_url_kwarg = "id"
    success_message = "Пользователь успешно изменен"


class UserDeleteView(LoginRequiredMixin, UserModificationMixin,
                     DeleteView):
    template_name = "users/delete.html"
    pk_url_kwarg = "id"
    success_message = "Пользователь успешно удален"

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "Пользователь успешно удален")

            return response
        except ProtectedError as e:
            messages.error(
                request, "Невозможно удалить пользователя, так как он связан с другими объектами."  # noqa E501
            )
            logger.error(f"ProtectedError when deleting user {self.object.id}: {e}")  # noqa: E501
            return self.get(request, *args, **kwargs)
