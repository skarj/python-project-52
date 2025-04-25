from django.db import models


class Status(models.Model):
    # TODO Статус нельзя удалить, если он связан хотя бы с одной задачей (сущность следующего шага)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
