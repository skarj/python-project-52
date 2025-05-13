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

    # to be able to update user without "user already exists" error
    def clean_username(self):
        return self.cleaned_data.get('username')
