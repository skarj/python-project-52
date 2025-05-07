import logging

from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.labels.forms import LabelCreateForm
from task_manager.labels.models import Label
from task_manager.mixins import LoginRequiredMixin

logger = logging.getLogger('django')


class LabelIndex(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"


class LabelCreateView(CreateView):
    model = Label
    form_class = LabelCreateForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels_index")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Метка успешно создана")
        return response


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelCreateForm
    template_name = "labels/update.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("labels_index")

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно изменена")
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("labels_index")

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "Метка успешно удалена")

            return response
        except ProtectedError as e:
            messages.error(
                request, "Невозможно удалить метку, потому что она используется"
            )
            logger.error(f"ProtectedError when deleting label {self.object.id}: {e}")  # noqa: E501
            return HttpResponseRedirect(self.success_url)
