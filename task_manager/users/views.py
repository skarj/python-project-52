import logging

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.mixins import LoginRequiredMixin
from task_manager.users import forms

logger = logging.getLogger('django')


class UserIndex(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, "users/index.html", {"users": users})


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
        messages.error(self.request, "У вас нет прав для изменения другого пользователя.")  # noqa E501
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
        messages.error(self.request, "У вас нет прав для изменения другого пользователя.")  # noqa E501
        return redirect("users_index")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, "Пользователь успешно удален")

            return response
        except ProtectedError as e:
            messages.error(
                request,
                "Невозможно удалить пользователя, потому что он используется"
            )
            logger.error(f"Failed to delete user. User ID: {self.object.id}. Error: {e}")  # noqa E501

            return redirect(self.success_url)
