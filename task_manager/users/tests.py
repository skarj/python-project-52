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


    def test_create_user(self):
        create_data = {
            "username": "ddefo",
            "first_name": "Daniel",
            "last_name": "Defo",
            "password1": self.password,
            "password2": self.password,
        }

        response = self.client.post(reverse("users_create"), data=create_data)
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username="ddefo")
        self.assertEqual(user.first_name, "Daniel")
        self.assertEqual(user.last_name, "Defo")

    def test_update_user(self):
        update_data = {
            "username": "jdaniel",
            "first_name": "Jack",
            "last_name": "Daniel",
            "password1": self.password,
            "password2": self.password,
        }

        response = self.client.post(
            reverse("users_update", kwargs={"id": self.user.id}),
            data=update_data,
        )
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "jdaniel")
        self.assertEqual(self.user.first_name, "Jack")
        self.assertEqual(self.user.last_name, "Daniel")

    def test_delete_user(self):
        response = self.client.post(
            reverse("users_delete", kwargs={"id": self.user.id})
        )
        self.assertEqual(response.status_code, 302)

        self.assertFalse(User.objects.filter(pk=self.user.id).exists())
