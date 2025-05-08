from django import forms
from django.contrib.auth.forms import UserCreationForm

from task_manager.users.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username"
        )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # TODO ?
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():  # noqa E501
            raise forms.ValidationError("Пользователь с таким именем уже существует.")  # noqa E501
        return username
