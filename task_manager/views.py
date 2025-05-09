from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class LoginView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"
    next_page = "index"
    success_message = "Вы залогинены"


class LogoutView(LogoutView):
    next_page = "index"

    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)
