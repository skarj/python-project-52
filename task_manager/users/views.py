import logging

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.mixins import LoginRequiredMixin
from task_manager.users import forms
from task_manager.users.models import User

logger = logging.getLogger('django')


class UserIndex(ListView):
    model = User
    template_name = "users/index.html"


class UserCreateView(CreateView):
    model = User
    form_class = forms.UserCreateForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Пользователь успешно зарегистрирован")
        return response


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = forms.UserCreateForm
    template_name = "users/update.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("users_index")

    def test_func(self):
        return self.request.user.id == self.kwargs.get("id")

    def handle_no_permission(self):
        messages.error(
            self.request, "У вас нет прав для изменения другого пользователя."
        )
        return redirect("users_index")

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно изменен")
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("users_index")

    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        messages.error(
            self.request, "У вас нет прав для изменения другого пользователя."
        )
        return redirect("users_index")

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
