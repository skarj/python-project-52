from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from task_manager.labels.forms import LabelCreateForm
from task_manager.labels.models import Label
from task_manager.mixins import LoginRequiredMixin


class LabelIndex(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(
            request,
            'labels/index.html',
            {'labels': labels}
        )

class LabelCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = LabelCreateForm()

        return render(
            request, 'labels/create.html', {'form': form}
        )

    def post(self, request, *args, **kwargs):
        form = LabelCreateForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Метка успешно cоздана'
            )
            return redirect('labels_index')

        return render(
            request, 'labels/create.html', {'form': form}
        )


class LabelDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = get_object_or_404(Label, id=label_id)

        return render(
            request, 'labels/delete.html', {'label': label}
        )

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = get_object_or_404(Label, id=label_id)

        try:
            label.delete()
            messages.success(
                request, 'Метка успешно удалена'
            )
        except ProtectedError:
            messages.error(request, 'Невозможно удалить метку, потому что она используется')

        return redirect('labels_index')


class LabelUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = get_object_or_404(Label, id=label_id)
        form = LabelCreateForm(instance=label)

        return render(
            request, 'labels/update.html', {'form': form}
        )

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = get_object_or_404(Label, id=label_id)
        form = LabelCreateForm(request.POST, instance=label)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Метка успешно изменена'
            )

            return redirect('labels_index')

        return render(
            request, 'labels/update.html', {'form': form}
        )
