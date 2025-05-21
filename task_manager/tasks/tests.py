from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


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

        self.user2 = User.objects.create(
            first_name="jdaniel",
            last_name="Jack",
            username="Daniel",
        )
        self.user2.set_password(self.password)
        self.user2.save()
        self.client.login(username=self.user.username, password=self.password)

    def test_create_tasks(self):
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

    def test_update_tasks(self):
        intial_status = Status.objects.create(
            name='Not Started'
        )

        updated_status = Status.objects.create(
            name='In Progress'
        )

        first_label = Label.objects.create(
            name='P1'
        )

        second_label = Label.objects.create(
            name='P2'
        )

        create_data = {
            "name": "Task2",
            "description": "Description",
            "status": intial_status.id,
            "executor": self.user.id,
            "labels": [first_label.id],
        }

        update_data = {
            "name": "Task22",
            "description": "Description2",
            "status": updated_status.id,
            "executor": self.user2.id,
            "labels": [first_label.id, second_label.id],
        }

        self.client.post(
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
        self.assertEqual(task.status, updated_status)
        self.assertEqual(task.executor.id, update_data["executor"])
        self.assertIn(first_label, task.labels.all())
        self.assertIn(second_label, task.labels.all())
        self.assertEqual(task.labels.count(), 2)

    def test_delete_tasks(self):
        status = Status.objects.create(
            name='In Discovery'
        )

        create_data = {
            "name": "Task3",
            "description": "Description",
            "status": status.id,
        }

        self.client.post(
            reverse("tasks_create"),
            data=create_data
        )
        task = Task.objects.get(name=create_data["name"])

        response = self.client.post(
            reverse("tasks_delete", kwargs={"id": task.id})
        )
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Task.objects.filter(pk=task.id).exists())

    def test_delete_not_owned_tasks(self):
        status = Status.objects.create(
            name='Blocked'
        )

        create_data = {
            "name": "Task4",
            "description": "Description",
            "status": status.id,
        }

        self.client.post(
            reverse("tasks_create"),
            data=create_data
        )

        self.client.logout()
        self.client.login(username=self.user2.username, password=self.password)

        task = Task.objects.get(name=create_data["name"])

        response = self.client.post(
            reverse("tasks_delete", kwargs={"id": task.id})
        )
        self.assertEqual(response.status_code, 302)

        self.assertTrue(Task.objects.filter(pk=task.id).exists())
