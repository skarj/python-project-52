from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from task_manager.mixins import LoginRequiredMixin
from task_manager.statuses.forms import StatusCreateForm
from task_manager.statuses.models import Status


class StatusIndex(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, "statuses/index.html", {"statuses": statuses})


class StatusCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = StatusCreateForm()

        return render(request, "statuses/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = StatusCreateForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Статус успешно создан")
            return redirect("statuses_index")

        return render(request, "statuses/create.html", {"form": form})


class StatusDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get("id")
        status = get_object_or_404(Status, id=status_id)

        return render(request, "statuses/delete.html", {"status": status})

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("id")
        status = get_object_or_404(Status, id=status_id)

        try:
            status.delete()
            messages.success(request, "Статус успешно удален")
        except ProtectedError:
            messages.error(
                request, "Невозможно удалить статус, потому что он используется"
            )

        return redirect("statuses_index")


class StatusUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get("id")
        status = get_object_or_404(Status, id=status_id)
        form = StatusCreateForm(instance=status)

        return render(request, "statuses/update.html", {"form": form})

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("id")
        status = get_object_or_404(Status, id=status_id)
        form = StatusCreateForm(request.POST, instance=status)

        if form.is_valid():
            form.save()
            messages.success(request, "Статус успешно изменен")

            return redirect("statuses_index")

        return render(request, "statuses/update.html", {"form": form})
