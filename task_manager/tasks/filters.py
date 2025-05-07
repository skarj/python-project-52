import django_filters
from django import forms

from .models import Task


class LabeledModelChoiceFilter(django_filters.ModelChoiceFilter):
    def __init__(self, *args, **kwargs):
        self.label_from_instance = kwargs.pop('label_from_instance', None)
        super().__init__(*args, **kwargs)

    @property
    def field(self):
        field = super().field
        if self.label_from_instance:
            field.label_from_instance = self.label_from_instance
        return field


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Task.status.field.related_model.objects.all(),
        required=False,
        label="Статус",
        widget=forms.Select(attrs={"class": "form-select ml-2 mr-3"})
    )
    executor = LabeledModelChoiceFilter(
        queryset=Task.executor.field.related_model.objects.all(),
        required=False,
        label="Исполнитель",
        widget=forms.Select(attrs={"class": "form-select ml-2 mr-3"}),
        label_from_instance=lambda obj: obj.full_name
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Task.labels.field.related_model.objects.all(),
        required=False,
        label="Метка",
        widget=forms.Select(attrs={"class": "form-select ml-2 mr-3"})
    )
    created_by_me = django_filters.BooleanFilter(
        required=False,
        method='filter_created_by_me',
        label='Только свои задачи',
        widget=forms.CheckboxInput(attrs={"class": "form-check-input mr-3"}),
        initial=False,
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_created_by_me(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
