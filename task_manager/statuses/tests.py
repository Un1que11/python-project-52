from django.test import TestCase
from django.urls import reverse

from task_manager.json_data import get_data
from task_manager.statuses.models import Status
from task_manager.users.models import User


class StatusTests(TestCase):
    fixtures = ['statuses.json']

    def setUp(self):
        self.statuses_url = reverse('statuses')
        self.status_create_url = reverse('status-create')
        self.user_info = get_data('users').get('new')
        self.status_info = get_data('statuses')

        self.create_user = User.objects.create_user(**self.user_info)
        self.create_user.save()

        self.client.login(
                username=self.user_info.get('username'),
                password=self.user_info.get('password')
                )

        existing_status = Status.objects.get(
                name=self.status_info.get('existing')['name']
                )
        self.status_update_url = reverse(
                'status-update',
                args=[existing_status.pk]
                )

        created_status = Status.objects.get(
                name=self.status_info.get('existing')['name']
                )
        self.status_delete_url = reverse(
                'status-delete',
                args=[created_status.pk]
                )

    def test_redirect_if_not_logged_in(self):
        self.client.logout()

        response = self.client.get(self.statuses_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/statuses/')

    def test_logged_in_user(self):
        response = self.client.get(self.statuses_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/show.html')

    def test_create_status(self):
        response = self.client.get(self.status_create_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')

        new_status = self.status_info.get('new')

        post_response = self.client.post(
                self.status_create_url,
                data={
                    'name': new_status
                    }
                )
        self.assertRedirects(post_response, self.statuses_url)

        created_status = Status.objects.get(name=new_status['name'])
        self.assertEquals(created_status.name, new_status['name'])

    def test_update_status(self):
        response = self.client.get(self.status_update_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')

        updated_status = self.status_info.get('new')
        post_response = self.client.post(
                self.status_update_url,
                data={
                    'name': updated_status
                    }
                )
        self.assertEquals(post_response.status_code, 302)

        status = Status.objects.get(name=updated_status['name'])
        self.assertEquals(updated_status['name'], status.name)

    def test_delete_status(self):
        response = self.client.get(self.status_delete_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete.html')

        post_response = self.client.post(self.status_delete_url)
        self.assertEquals(post_response.status_code, 302)
        self.assertRedirects(response, self.statuses_url)
