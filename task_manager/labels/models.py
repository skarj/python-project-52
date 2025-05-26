from django.db import models

from task_manager.models import TimeStampedModel


class Label(TimeStampedModel):
    name = models.CharField(
        "Имя",
        max_length=255,
        unique=True
    )

    def __str__(self):
        return self.name
