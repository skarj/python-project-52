from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="Имя",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Имя"
        }),
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Фамилия",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Фамилия"}
        ),
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Имя пользователя",
        help_text="Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.",  # noqa: E501
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Имя пользователя"}
        ),
    )
    password1 = forms.CharField(
        required=True,
        label="Пароль",
        help_text="Ваш пароль должен содержать как минимум 3 символа.",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        ),
    )
    password2 = forms.CharField(
        required=True,
        label="Подтверждение пароля",
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз.",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Подтверждение пароля"
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2"
        )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():  # noqa E501
            raise forms.ValidationError("Пользователь с таким именем уже существует.")  # noqa E501
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        is_bound = self.is_bound

        for name, field in self.fields.items():
            if is_bound:
                if self.errors.get(name):
                    field.widget.attrs["class"] += " is-invalid"
                else:
                    field.widget.attrs["class"] += " is-valid"
