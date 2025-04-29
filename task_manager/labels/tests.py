from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label


class TestUsers(TestCase):
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
        create_data = {
            'name': 'WIP',
        }

        update_data = {
            'name': 'Iteration 1',
        }

        self.client.post(
            reverse('labels_create'),
            data=create_data
        )

        status = Label.objects.get(name=create_data['name'])
        self.assertEqual(status.name, create_data['name'])

        self.client.post(
            reverse('labels_update', kwargs={'id': status.id}),
            data=update_data
        )

        status.refresh_from_db()
        self.assertEqual(status.name, update_data['name'])

        self.client.post(
            reverse('labels_delete', kwargs={'id': status.id}),
        )

        self.assertFalse(Label.objects.filter(pk=status.id).exists())
