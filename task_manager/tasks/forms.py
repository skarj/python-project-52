from django.forms import ModelForm

from task_manager.tasks.models import Task


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task

        fields = [
            "name",
            "description",
            "status",
            "executor",
            "labels"
        ]

    # Change label for executor field to full name
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].label_from_instance = lambda obj: f'{obj.first_name} {obj.last_name}'  # noqa: E501
