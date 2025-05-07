import logging

from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.mixins import LoginRequiredMixin
from task_manager.statuses.forms import StatusCreateForm
from task_manager.statuses.models import Status

logger = logging.getLogger('django')


class StatusIndex(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusCreateForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses_index")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Статус успешно создан")
        return response


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusCreateForm
    template_name = "statuses/update.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("statuses_index")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно изменен")
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("statuses_index")

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "Статус успешно удален")

            return response
        except ProtectedError as e:
            messages.error(
                request, "Невозможно удалить статус, потому что он используется"
            )
            logger.error(f"ProtectedError when deleting status {self.object.id}: {e}")  # noqa: E501
            return HttpResponseRedirect(self.success_url)
