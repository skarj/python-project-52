from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from task_manager.mixins import LoginRequiredMixin
from task_manager.tasks.forms import TaskCreateForm, TaskFilterForm
from task_manager.tasks.models import Task


class TaskIndex(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        filter_form = TaskFilterForm(request.GET)

        if filter_form.is_valid():
            status = filter_form.cleaned_data.get('status')
            assigned_to = filter_form.cleaned_data.get('assigned_to')
            assigned_to_me = filter_form.cleaned_data.get('assigned_to_me')

            if status:
                tasks = tasks.filter(status=status)
            if assigned_to:
                tasks = tasks.filter(assigned_to=assigned_to)
            if assigned_to_me:
                tasks = tasks.filter(author=request.user.id)

        return render(
            request,
            'tasks/index.html',
            {'tasks': tasks, 'form': filter_form}
        )

class TaskCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TaskCreateForm()

        return render(
            request, 'tasks/create.html', {'form': form}
        )

    def post(self, request, *args, **kwargs):
        form = TaskCreateForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()

            messages.success(
                request, "Задача успешно создана"
            )
            return redirect('tasks_index')

        return render(
            request, 'tasks/create.html', {'form': form}
        )


class TaskDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = get_object_or_404(Task, id=task_id)

        if request.user.id != task.author.id:
            messages.error(
                request, 'Задачу может удалить только ее автор'
            )

            return redirect('tasks_index')

        return render(
            request, 'tasks/delete.html', {'task': task}
        )

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        messages.success(
            request, 'Задача успешно удалена'
        )

        return redirect('tasks_index')


class TaskUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        task = get_object_or_404(Task, id=task_id)
        form = TaskCreateForm(instance=task)

        return render(
            request, 'tasks/update.html', {'form': form}
        )

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = get_object_or_404(Task, id=task_id)
        form = TaskCreateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Задача успешно изменена'
            )

            return redirect('tasks_index')

        return render(
            request, 'tasks/update.html', {'form': form}
        )
