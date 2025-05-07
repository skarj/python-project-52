from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.users.models import User


class TestStatuses(TestCase):
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
        create_data = {
            "name": "In Progress",
        }

        response = self.client.post(
            reverse("statuses_create"),
            data=create_data
        )
        self.assertEqual(response.status_code, 302)

        status = Status.objects.get(name=create_data["name"])
        self.assertEqual(status.name, create_data["name"])

    def test_update_status(self):
        status = Status.objects.create(
            name='Closed'
        )

        update_data = {
            "name": "Resolved",
        }

        response = self.client.post(
            reverse("statuses_update", kwargs={"id": status.id}),
            data=update_data,
        )
        self.assertEqual(response.status_code, 302)

        status.refresh_from_db()
        self.assertEqual(status.name, update_data["name"])

    def test_delete_status(self):
        status = Status.objects.create(
            name='In Descovery'
        )

        response = self.client.post(
            reverse("statuses_delete", kwargs={"id": status.id})
        )
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Status.objects.filter(pk=status.id).exists())
