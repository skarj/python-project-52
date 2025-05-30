from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import LoginRequiredMixin, OwnershipRequiredMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskCreateForm
from task_manager.tasks.models import Task


class TaskIndexView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter
    queryset = Task.objects.select_related("author", "executor", "status")

class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks_index")
    success_message = "Задача успешно создана"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                     UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/update.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("tasks_index")
    success_message = "Задача успешно изменена"


class TaskDeleteView(SuccessMessageMixin, OwnershipRequiredMixin,
                     LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("tasks_index")
    permission_denied_redirect_url = "tasks_index"
    template_name = "tasks/delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("tasks_index")
    success_message = "Задача успешно удалена"
    permission_denied_message = "Задачу может удалить только ее автор"
    ownership_field = 'author'


class TaskShowView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/show.html"
    context_object_name = "task"
    pk_url_kwarg = "id"
    queryset = Task.objects.select_related(
        "author",
        "executor",
        "status"
    ).prefetch_related("labels")
