from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TestTasks(TestCase):
    password = "testpass123"

    def setUp(self):
        self.user = User.objects.create(
            first_name="Jack",
            last_name="Black",
            username="jblack",
        )
        self.user.set_password(self.password)
        self.user.save()
        self.client.login(username=self.user.username, password=self.password)

    def test_create_status(self):
        status = Status.objects.create(
            name='Not Started'
        )

        create_data = {
            "name": "Task1",
            "description": "Description",
            "status": status.id,
        }

        response = self.client.post(
            reverse("tasks_create"),
            data=create_data
        )
        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(name=create_data["name"])
        self.assertEqual(task.name, create_data["name"])

    def test_update_status(self):
        status = Status.objects.create(
            name='New'
        )

        create_data = {
            "name": "Task2",
            "description": "Description",
            "status": status.id,
        }

        update_data = {
            "name": "Task22",
            "description": "Description2",
            "status": status.id,
        }

        response = self.client.post(
            reverse("tasks_create"),
            data=create_data
        )
        task = Task.objects.get(name=create_data["name"])

        response = self.client.post(
            reverse("tasks_update", kwargs={"id": task.id}),
            data=update_data,
        )
        self.assertEqual(response.status_code, 302)

        task.refresh_from_db()
        self.assertEqual(task.name, update_data["name"])
        self.assertEqual(task.description, update_data["description"])

    def test_delete_status(self):
        status = Status.objects.create(
            name='In Discovery'
        )

        create_data = {
            "name": "Task3",
            "description": "Description",
            "status": status.id,
        }
        response = self.client.post(
            reverse("tasks_create"),
            data=create_data
        )
        task = Task.objects.get(name=create_data["name"])

        response = self.client.post(
            reverse("tasks_delete", kwargs={"id": task.id})
        )
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Task.objects.filter(pk=task.id).exists())
