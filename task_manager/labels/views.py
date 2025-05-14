from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.labels.forms import LabelCreateForm
from task_manager.labels.models import Label
from task_manager.mixins import LoginRequiredMixin, ProtectedDeleteMixin


class LabelIndex(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"


class LabelCreateView(SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelCreateForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels_index")
    success_message = "Метка успешно создана"


class LabelUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                      UpdateView):
    model = Label
    form_class = LabelCreateForm
    template_name = "labels/update.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("labels_index")
    success_message = "Метка успешно изменена"


class LabelDeleteView(LoginRequiredMixin, ProtectedDeleteMixin,
                      DeleteView):
    model = Label
    template_name = "labels/delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("labels_index")
    success_message = "Метка успешно удалена"
    protected_error_message = "Невозможно удалить метку, потому что она используется"  # noqa E501
