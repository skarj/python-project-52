from django import forms
from django.contrib.auth.forms import UserCreationForm

from task_manager.users.models import User


class UserCreateForm(UserCreationForm):
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username"
        )


class UserUpdateForm(UserCreateForm):
    class Meta(UserCreateForm.Meta):
        fields = UserCreateForm.Meta.fields

    #  to be able to update user without "user already exists" error
    def clean_username(self):
        return self.cleaned_data.get('username')
