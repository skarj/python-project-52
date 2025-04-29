from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status


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

    def test_create_update_delete_status(self):
        create_data = {
            "name": "In Progress",
        }

        update_data = {
            "name": "Resolved",
        }

        self.client.post(reverse("statuses_create"), data=create_data)

        status = Status.objects.get(name=create_data["name"])
        self.assertEqual(status.name, create_data["name"])

        self.client.post(
            reverse("statuses_update", kwargs={"id": status.id}), data=update_data
        )

        status.refresh_from_db()
        self.assertEqual(status.name, update_data["name"])

        self.client.post(
            reverse("statuses_delete", kwargs={"id": status.id}),
        )

        self.assertFalse(Status.objects.filter(pk=status.id).exists())
