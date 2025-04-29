from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TestTasks(TestCase):
    password = 'testpass123'

    def setUp(self):
        self.user = User.objects.create(
            first_name='Jack',
            last_name='Black',
            username='jblack',
        )

        self.user.set_password(self.password)
        self.user.save()

        self.client.login(
            username=self.user.username,
            password=self.password
        )

    def test_create_update_delete_status(self):
        status = Status(name='status')
        status.save()

        create_data = {
            'name': 'Task1',
            'description': 'Description',
            'status': status.id,
        }

        update_data = {
            'name': 'Task2',
            'description': 'Description2',
            'status': status.id,
        }

        self.client.post(
            reverse('tasks_create'),
            data=create_data
        )

        task = Task.objects.get(name=create_data['name'])
        self.assertEqual(task.name, create_data['name'])

        self.client.post(
            reverse('tasks_update', kwargs={'id': task.id}),
            data=update_data
        )

        task.refresh_from_db()
        self.assertEqual(task.name, update_data['name'])
        self.assertEqual(task.description, update_data['description'])

        self.client.post(
            reverse('tasks_delete', kwargs={'id': status.id}),
        )

        self.assertFalse(Task.objects.filter(pk=status.id).exists())
