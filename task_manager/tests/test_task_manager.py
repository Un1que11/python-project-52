from django.utils.translation import gettext_lazy as _
from django.test import TestCase, Client
from django.contrib.auth import SESSION_KEY
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.http import HttpResponse

from http import HTTPStatus
from dataclasses import dataclass
from typing import Dict, Tuple

from task_manager.users.models import User


class HomePageTest(TestCase):

    fixtures = ['user.json']

    def test_user_update_view(self) -> None:
        ROUTE = reverse_lazy('home')

        response: HttpResponse = self.client.get(ROUTE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name='index.html')


class AuthenticationTest(TestCase):

    fixtures = ['user.json']

    def setUp(self) -> None:
        self.client: Client = Client()
        self.credentials: Dict[str, str] = {
            'username': 'testuser',
            'password': 'secret_password'
        }
        self.user: User = User.objects.create_user(**self.credentials)

    def test_login(self) -> None:
        # Send login data and checking if a redirect exists
        response: HttpResponse = self.client.post(
            reverse_lazy('login'), self.credentials, follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse_lazy('home'))
        # Should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self) -> None:
        # Log in and make sure the session is valid
        self.client.login(**self.credentials)
        self.assertTrue(SESSION_KEY in self.client.session)
        # There should be no session key on exit
        response: HttpResponse = self.client.get(reverse_lazy('logout'))
        self.assertTrue(SESSION_KEY not in self.client.session)
        # Checking if a redirect exists
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse_lazy('home'))


class PagesAccessibility(TestCase):

    fixtures = ['task.json', 'label.json', 'status.json', 'user.json']

    def setUp(self) -> None:
        self.unauthenticated_client: Client = Client()
        self.authenticated_client: Client = Client()
        self.authenticated_client.force_login(User.objects.get(pk=1))

    def test_unavailability_of_viewing_by_unauthenticated_users(self) -> None:

        @dataclass
        class NotAllowedPageRoutes:
            with_pk: Tuple[str] = (
                'status_update', 'status_delete',
                'task_update', 'task_delete', 'task_detail',
                'label_update', 'label_delete'
            )
            without_pk: Tuple[str] = (
                'statuses', 'status_create',
                'tasks', 'task_create',
                'labels', 'label_create'
            )
            _all: Tuple[str] = with_pk + without_pk

        for not_allowed_page_route in NotAllowedPageRoutes._all:
            if not_allowed_page_route in NotAllowedPageRoutes.with_pk:
                response: HttpResponse = self.unauthenticated_client.get(
                    reverse_lazy(not_allowed_page_route, args=[1])
                )
            elif not_allowed_page_route in NotAllowedPageRoutes.without_pk:
                response: HttpResponse = self.unauthenticated_client.get(
                    reverse_lazy(not_allowed_page_route)
                )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertRaisesMessage(
            expected_exception=PermissionDenied,
            expected_message=_('You are not authorized! Please sign in.')
        )

    def test_prohibition_of_changing_user_info_by_another_user(self) -> None:
        inaccessible_id: int = 2  # recall that we are a client with ID 1
        for route in ('user_update', 'user_delete'):
            response: HttpResponse = self.authenticated_client.get(
                reverse_lazy(route, args=[inaccessible_id])
            )
            self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_unavailability_of_task_deletion_by_non_authors(self) -> None:
        response: HttpResponse = self.authenticated_client.get(
            'task_delete', args=[1]
        )  # the task author must not be the same as the user's client under test

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
