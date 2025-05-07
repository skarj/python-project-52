from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import LoginRequiredMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskCreateForm
from task_manager.tasks.models import Task


class TaskIndex(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = context["filter"].form
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks_index")

    def form_valid(self, form):
        task = form.save(commit=False)
        task.author = self.request.user
        task.save()
        form.save_m2m()
        messages.success(self.request, "Задача успешно создана")
        return redirect(self.success_url)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/update.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("tasks_index")

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно изменена")
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("tasks_index")

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(self.request, "Задачу может удалить только ее автор")
        return redirect("tasks_index")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, "Задача успешно удалена")

        return response


class TaskShowView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/show.html"
    context_object_name = "task"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["labels"] = self.object.labels.all()
        return context
