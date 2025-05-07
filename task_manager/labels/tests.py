from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label


class TestLabels(TestCase):
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

    def test_create_label(self):
        create_data = {
            "name": "WiP",
        }

        response = self.client.post(reverse("labels_create"), data=create_data)
        self.assertEqual(response.status_code, 302)

        label = Label.objects.get(name=create_data["name"])
        self.assertEqual(label.name, create_data["name"])

    def test_update_label(self):
        label = Label.objects.create(
            name='P1'
        )

        update_data = {
            "name": "P2",
        }

        response = self.client.post(
            reverse("labels_update", kwargs={"id": label.id}),
            data=update_data,
        )
        self.assertEqual(response.status_code, 302)

        label.refresh_from_db()
        self.assertEqual(label.name, update_data["name"])

    def test_delete_label(self):
        label = Label.objects.create(
            name='P0'
        )

        response = self.client.post(
            reverse("labels_delete", kwargs={"id": label.id})
        )
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Label.objects.filter(pk=label.id).exists())
