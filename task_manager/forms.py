from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        is_bound = self.is_bound

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if is_bound:
                if self.errors.get(name):
                    field.widget.attrs['class'] += ' is-invalid'
                else:
                    field.widget.attrs['class'] += ' is-valid'
