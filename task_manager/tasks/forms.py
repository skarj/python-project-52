from django import forms
from django.contrib.auth.models import User

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


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

    executor = forms.ModelChoiceField(
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
            field.widget.attrs["class"] = "form-control"
            if is_bound:
                if self.errors.get(name):
                    field.widget.attrs["class"] += " is-invalid"
                else:
                    field.widget.attrs["class"] += " is-valid"

        # Custom labels for User dropdown
        self.fields["executor"].label_from_instance = (
            lambda obj: f"{obj.first_name} {obj.last_name}"
        )


class TaskFilterForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label="Статус",
        widget=forms.Select(attrs={"class": "form-select ml-2 mr-3"}),
    )

    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Исполнитель",
        widget=forms.Select(attrs={"class": "form-select ml-2 mr-3"}),
    )

    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label="Метка",
        widget=forms.Select(attrs={"class": "form-select ml-2 mr-3"}),
    )

    created_by_me = forms.BooleanField(
        required=False,
        label="Только свои задачи",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input mr-3"}),
        initial=False,
    )

    class Meta:
        model = Task
        fields = ("status", "executor")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Custom labels for User dropdown
        self.fields["executor"].label_from_instance = (
            lambda obj: f"{obj.first_name} {obj.last_name}"
        )
