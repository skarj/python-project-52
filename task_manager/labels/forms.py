from django import forms

from task_manager.labels.models import Label


class LabelCreateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Имя",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Имя"}
        ),
    )

    class Meta:
        model = Label
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        is_bound = self.is_bound

        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            if is_bound:
                if self.errors.get(name):
                    field.widget.attrs["class"] += " is-invalid"
                else:
                    field.widget.attrs["class"] += " is-valid"
