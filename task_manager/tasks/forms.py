from django import forms

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.full_name


class TaskCreateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Имя",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Имя"
        }),
    )

    description = forms.CharField(
        max_length=150,
        label="Описание",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Описание"}
        ),
    )

    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=True,
        label="Статус",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    executor = UserModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Исполнитель",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label="Метки",
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 4}),
    )

    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        is_bound = self.is_bound

        # Customize field class
        for name, field in self.fields.items():
            if is_bound:
                if self.errors.get(name):
                    field.widget.attrs["class"] += " is-invalid"
                else:
                    field.widget.attrs["class"] += " is-valid"
