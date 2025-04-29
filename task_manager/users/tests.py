from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestUsers(TestCase):
    password = "testpass123"

    def setUp(self):
        self.user = User.objects.create(
            first_name="Jack",
            last_name="Black",
            username="jblack",
        )

        self.user.set_password(self.password)
        self.user.save()

        self.client.login(username="jblack", password=self.password)

    def test_create_update_delete_user(self):
        create_data = {
            "username": "ddefo",
            "first_name": "Daniel",
            "last_name": "Defo",
            "password1": self.password,
            "password2": self.password,
        }

        update_data = {
            "username": "jdaniel",
            "first_name": "Jack",
            "last_name": "Daniel",
            "password1": self.password,
            "password2": self.password,
        }

        self.client.post(reverse("users_create"), data=create_data)

        user = User.objects.get(username="ddefo")
        self.assertEqual(user.username, "ddefo")
        self.assertEqual(user.first_name, "Daniel")
        self.assertEqual(user.last_name, "Defo")

        self.client.post(
            reverse("users_update", kwargs={"id": user.id}), data=update_data
        )

        user.refresh_from_db()
        self.assertEqual(user.username, "jdaniel")
        self.assertEqual(user.first_name, "Jack")
        self.assertEqual(user.last_name, "Daniel")

        self.client.post(
            reverse("users_delete", kwargs={"id": user.id}),
        )

        self.assertFalse(User.objects.filter(pk=user.id).exists())
