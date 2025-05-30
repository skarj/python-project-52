import logging

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.mixins import (
    LoginRequiredMixin,
    OwnershipRequiredMixin,
    ProtectedDeleteMixin,
)
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


class UserUpdateView(SuccessMessageMixin, OwnershipRequiredMixin,
                     LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy("users_index")
    permission_denied_redirect_url = reverse_lazy("users_index")
    template_name = "users/update.html"
    form_class = forms.UserUpdateForm
    pk_url_kwarg = "id"
    success_message = "Пользователь успешно изменен"
    permission_denied_message = "У вас нет прав для изменения другого пользователя."  # noqa E501


class UserDeleteView(SuccessMessageMixin, OwnershipRequiredMixin,
                     LoginRequiredMixin, ProtectedDeleteMixin,
                     DeleteView):
    model = User
    success_url = reverse_lazy("users_index")
    permission_denied_redirect_url = reverse_lazy("users_index")
    template_name = "users/delete.html"
    pk_url_kwarg = "id"
    success_message = "Пользователь успешно удален"
    protected_error_message = "Невозможно удалить пользователя, так как он связан с другими объектами."  # noqa E501
    permission_denied_message = "У вас нет прав для изменения другого пользователя."  # noqa E501
