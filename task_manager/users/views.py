from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
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
            messages.success(request, "Пользователь успешно зарегистрирован")
            # user = form.save()
            # login(request, user)
            return redirect('users_index')

        return render(
            request, 'users/create.html', {'form': form}
        )

class UserDeleteView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)

        return render(
            request, 'users/delete.html', {'user': user}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
            messages.success(
                request, 'Пользователь успешно удален'
            )

        return redirect('users_index')
