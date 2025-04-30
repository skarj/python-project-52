from django.contrib.auth.models import User
from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    author = models.ForeignKey(
        User, related_name="authored_tasks", on_delete=models.PROTECT
    )
    executor = models.ForeignKey(
        User,
        related_name="assigned_tasks",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    labels = models.ManyToManyField(Label, through="LabelTask")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LabelTask(models.Model):
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
