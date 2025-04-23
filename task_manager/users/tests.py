from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User



# class TestUsers(TestCase):
#     def test_users_list(self):
#         response = self.client.get(reverse('users_index'))
#         self.assertEqual(response.status_code, 200)

#         self.assertIn('users', response.context)
#         users = response.context['users']

#         self.assertTrue(len(users) > 0)


class UsersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name='Jack',
            last_name='Black',
            username='jblack',
            # password1='123',
            # password2='123'
        )

    def test_update_user(self):
        user_id = self.user.pk

        update_data = {
            'username': 'jackblack',
        }

        response = self.client.post(
            reverse('users_update', kwargs={'id': user_id}),
            data=update_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.context['user'].username, 'jackblack')
