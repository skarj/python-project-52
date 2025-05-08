from django import forms
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter
from task_manager.users.models import User

from .models import Task


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(
        queryset=Task.status.field.related_model.objects.all(),
        label="Статус",
    )

    executor = ModelChoiceFilter(
        queryset=Task.executor.field.related_model.objects.all(),
        label="Исполнитель",
    )

    labels = ModelChoiceFilter(
        queryset=Task.labels.field.related_model.objects.all(),
        label="Метка",
    )

    created_by_me = BooleanFilter(
        method='filter_created_by_me',
        label='Только свои задачи',
        widget=forms.CheckboxInput(),
        initial=False,
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_created_by_me(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
