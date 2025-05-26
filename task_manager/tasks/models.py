from django.db import models

from task_manager.labels.models import Label
from task_manager.models import TimeStampedModel
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(TimeStampedModel):
    name = models.CharField(
        "Имя",
        max_length=255,
        unique=True
    )

    description = models.TextField(
        "Описание",
        max_length=255
    )

    author = models.ForeignKey(
        User,
        related_name="authored_tasks",
        on_delete=models.PROTECT
    )

    executor = models.ForeignKey(
        User,
        verbose_name="Исполнитель",
        related_name="assigned_tasks",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    status = models.ForeignKey(
        Status,
        verbose_name="Статус",
        on_delete=models.PROTECT
    )

    labels = models.ManyToManyField(
        Label,
        verbose_name="Метки",
        through="LabelTask",
        blank=True
    )


class LabelTask(models.Model):
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
