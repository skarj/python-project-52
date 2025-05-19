
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.mixins import LoginRequiredMixin, ProtectedDeleteMixin
from task_manager.statuses.forms import StatusCreateForm
from task_manager.statuses.models import Status


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


class StatusDeleteView(SuccessMessageMixin, LoginRequiredMixin,
                       ProtectedDeleteMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("statuses_index")
    success_message = "Статус успешно удален"
    protected_error_message = "Невозможно удалить статус, потому что он используется"  # noqa E501
