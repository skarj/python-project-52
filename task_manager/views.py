from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views import View

from task_manager import forms


class IndexView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'index.html')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()

        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('index')

        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(
            request, 'Вы разлогинены'
        )

        return redirect('index')
