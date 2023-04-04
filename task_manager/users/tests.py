from django import test
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.json_data import get_data
from task_manager.users.models import User


class UserTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.home_url = reverse('home')
        self.users_list_url = reverse('users-list')
        self.user_register_url = reverse('register')
        self.user_login_url = reverse('login')

        self.user_info = get_data('users').get('new')
        self.users_info = get_data('users')

        self.create_user = User.objects.create_user(**self.users_info.get('new'))
        self.create_user.save()

        self.user_update_url = reverse('update', args=[self.create_user.id])
        self.user_delete_url = reverse('delete', args=[self.create_user.id])

    def login(self):
        self.client.login(
                username=self.user_info.get('username'),
                password=self.user_info.get('password')
            )

    def assertUser(self, user, user_data):
        self.assertEqual(
                user.first_name,
                user_data.get('first_name')
                )
        self.assertEqual(
                user.last_name,
                user_data.get('last_name')
                )

    def test_home_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_users_list_GET(self):
        response = self.client.get(self.users_list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/show.html')

    def test_user_register_GET(self):
        response = self.client.get(self.user_register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_login_GET(self):
        response = self.client.get(self.user_login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

        exist_user = {
                'id': self.user_info.get('id'),
                'username': self.user_info.get('username'),
                'password': self.user_info.get('password')
                }

        tester_login = self.client.login(**exist_user)

        self.assertTrue(tester_login)
        self.client.logout()

        response = self.client.post(self.user_login_url, exist_user, follow=True)

        self.assertTrue(response.context['user'].is_active)
        self.assertEquals(
                int(self.client.session['_auth_user_id']),
                exist_user.get('id')
                )

    def test_user_update_GET(self):
        self.login()
        response = self.client.get(self.user_update_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')

    def test_user_delete_GET(self):
        self.login()
        response = self.client.get(self.user_delete_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')

    def test_user_register_POST(self):
        response = self.client.post(
                self.user_register_url,
                self.users_info.get('tester')
                )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.user_login_url)

        response = self.client.post(
                self.user_register_url,
                self.users_info.get('new')
                )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_update_POST(self):
        self.login()
        update_user_info = self.users_info.get('updated_user')

        response = self.client.post(self.user_update_url, update_user_info)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.users_list_url)

        updated_user = get_user_model().objects.get(
                username=update_user_info.get('username')
                )

        self.assertUser(updated_user, update_user_info)

    def test_user_delete_POST(self):
        self.login()
        response = self.client.post(self.user_delete_url)

        self.assertRedirects(response, self.users_list_url)
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.login()
        response = self.client.post(reverse('logout'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
