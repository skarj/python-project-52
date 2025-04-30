from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from task_manager.mixins import LoginRequiredMixin
from task_manager.users import forms


class UserIndex(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, "users/index.html", {"users": users})


class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        form = forms.UserCreateForm()

        return render(request, "users/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = forms.UserCreateForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно зарегистрирован")
            return redirect("login")

        return render(request, "users/create.html", {"form": form})


class UserDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = get_object_or_404(User, id=user_id)

        if request.user.id != user_id:
            messages.error(
                request, "У вас нет прав для изменения другого пользователя."
            )

            return redirect("users_index")

        return render(request, "users/delete.html", {"user": user})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = get_object_or_404(User, id=user_id)

        try:
            user.delete()
            messages.success(request, "Пользователь успешно удален")
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить пользователя, потому что он используется"
            )

        return redirect("users_index")


class UserUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = get_object_or_404(User, id=user_id)
        form = forms.UserCreateForm(instance=user)

        if request.user.id != user_id:
            messages.error(
                request, "У вас нет прав для изменения другого пользователя."
            )

            return redirect("users_index")

        return render(request, "users/update.html", {"form": form})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = get_object_or_404(User, id=user_id)
        form = forms.UserCreateForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно изменен")

            return redirect("users_index")

        return render(request, "users/update.html", {"form": form})
