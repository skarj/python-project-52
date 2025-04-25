from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from django.test import TestCase
from django.urls import reverse

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
            username='jblack',
            password=self.password
        )

    def test_create_update_delete_status(self):
        create_data = {
            'name': 'In Progress',
        }

        update_data = {
            'name': 'Resolved',
        }

        self.client.post(
            reverse('statuses_create'),
            data=create_data
        )

        status = Status.objects.get(name='In Progress')
        self.assertEqual(status.name, 'In Progress')

        self.client.post(
            reverse('statuses_update', kwargs={'id': status.id}),
            data=update_data
        )

        status.refresh_from_db()
        self.assertEqual(status.name, 'Resolved')

        self.client.post(
            reverse('statuses_delete', kwargs={'id': status.id}),
        )

        self.assertFalse(Status.objects.filter(pk=status.id).exists())
