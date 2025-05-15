from django import forms
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.first_name} {obj.last_name}'


class UserModelChoiceFilter(ModelChoiceFilter):
    field_class = UserModelChoiceField


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label="Статус",
    )

    executor = UserModelChoiceFilter(
        queryset=User.objects.all(),
        label="Исполнитель",
    )

    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
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
