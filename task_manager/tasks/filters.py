from django import forms
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from .models import Task


# TODO: other way to show full_name
class LabeledModelChoiceFilter(ModelChoiceFilter):
    def __init__(self, *args, **kwargs):
        self.label_from_instance = kwargs.pop('label_from_instance', None)
        super().__init__(*args, **kwargs)

    @property
    def field(self):
        field = super().field
        if self.label_from_instance:
            field.label_from_instance = self.label_from_instance
        return field


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(
        queryset=Task.status.field.related_model.objects.all(),
        label="Статус",
    )

    executor = LabeledModelChoiceFilter(
        queryset=Task.executor.field.related_model.objects.all(),
        label="Исполнитель",
        label_from_instance=lambda obj: obj.full_name
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
