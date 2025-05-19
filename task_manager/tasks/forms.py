from django import forms
from django.forms import ModelForm

from task_manager.tasks.models import Task
from task_manager.users.models import User


# Change label for executor field to full name
class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.first_name} {obj.last_name}'


class TaskCreateForm(ModelForm):
    executor = UserModelChoiceField(
        queryset=User.objects.all(),
        label='Исполнитель',
        required=False
    )

    class Meta:
        model = Task

        fields = [
            "name",
            "description",
            "status",
            "executor",
            "labels"
        ]
