from django.contrib.auth.models import User
from django.shortcuts import redirect, render
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
            # user = form.save()
            # login(request, user)
            return redirect('users_index')

        return render(
            request, 'users/create.html', {'form': form}
        )
