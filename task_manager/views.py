from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from task_manager.forms import LoginForm
from task_manager.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = "index.html"


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    next_page = "index"

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    next_page = "index"

    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)
