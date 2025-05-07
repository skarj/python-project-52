from django.contrib.auth.models import User


class User(User):
    class Meta:
        proxy = True

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
