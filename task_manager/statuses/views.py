import logging

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
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


class StatusCreateView(SuccessMessageMixin, LoginRequiredMixin,
                       CreateView):
    model = Status
    form_class = StatusCreateForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses_index")
    success_message = "Статус успешно создан"


class StatusUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                        UpdateView):
    model = Status
    form_class = StatusCreateForm
    template_name = "statuses/update.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("statuses_index")
    success_message = "Статус успешно изменен"


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
