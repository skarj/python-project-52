from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404

from django.views import View

from task_manager.users import forms


def index(request):
    users = User.objects.all()
    return render(
        request,
        'users/index.html',
        {'users': users}
    )


class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        form = forms.UserCreateForm()

        return render(
            request, 'users/create.html', {'form': form}
        )

    def post(self, request, *args, **kwargs):
        form = forms.UserCreateForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, "Пользователь успешно зарегистрирован"
            )
            # user = form.save()
            # login(request, user)
            return redirect('users_index')

        return render(
            request, 'users/create.html', {'form': form}
        )

class UserDeleteView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, id=user_id)

        return render(
            request, 'users/delete.html', {'user': user}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(
            request, 'Пользователь успешно удален'
        )

        return redirect('users_index')


class UserUpdateView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = get_object_or_404(User, id=user_id)
        form = forms.UserCreateForm(instance=user)

        return render(
            request, 'users/update.html', {'form': form}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        form = forms.UserCreateForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Пользователь успешно изменен'
            )

            return redirect('users_index')

        return render(
            request, 'users/update.html', {'form': form}
        )
