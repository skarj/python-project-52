from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import User


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

        self.user2 = User.objects.create(
            first_name="jdaniel",
            last_name="Jack",
            username="Daniel",
        )
        self.user2.set_password(self.password)
        self.user2.save()

        self.client.force_login(self.user)

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

        user = User.objects.get(username=create_data["username"])
        self.assertEqual(user.first_name, create_data["first_name"])
        self.assertEqual(user.last_name, create_data["last_name"])
        self.assertTrue(user.check_password(create_data['password1']))

    def test_create_user_wo_lastname(self):
        create_data = {
            "username": "ddefo",
            "first_name": "Daniel",
            "last_name": "",
            "password1": self.password,
            "password2": self.password,
        }

        response = self.client.post(reverse("users_create"), data=create_data)
        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(User.objects.filter(username=create_data["username"]).exists())

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
        self.assertEqual(self.user.username, update_data["username"])
        self.assertEqual(self.user.first_name, update_data["first_name"])
        self.assertEqual(self.user.last_name, update_data["last_name"])

    def test_delete_user(self):
        response = self.client.post(
            reverse("users_delete", kwargs={"id": self.user.id})
        )
        self.assertEqual(response.status_code, 302)

        self.assertFalse(User.objects.filter(pk=self.user.id).exists())

    def test_delete_user_denied_to_other_users(self):
        self.client.logout()
        self.client.force_login(self.user2)

        response = self.client.post(
            reverse("users_delete", kwargs={"id": self.user.id})
        )
        self.assertEqual(response.status_code, 302)

        self.assertTrue(User.objects.filter(pk=self.user.id).exists())

    def test_update_user_denied_to_other_users(self):
        update_data = {
            "username": "jdaniel2",
            "password1": self.password,
            "password2": self.password,
        }

        self.client.logout()
        self.client.force_login(self.user2)

        self.client.post(
            reverse("users_update", kwargs={"id": self.user.id}),
            data=update_data,
        )
        self.assertEqual(self.user.username, "jblack")
