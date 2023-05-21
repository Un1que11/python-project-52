from django.test import TestCase, Client
from django.contrib.auth import SESSION_KEY
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.http import HttpResponse

from http import HTTPStatus
from dataclasses import dataclass
from typing import Dict, Tuple

from task_manager.users.models import User
from task_manager.constants import HOME, TEMPLATE_INDEX, \
    REVERSE_HOME, REVERSE_LOGIN, REVERSE_LOGOUT, MSG_NO_PERMISSION
from task_manager.users.constants import UPDATE_USER, DELETE_USER
from task_manager.statuses.constants import \
    LIST_STATUSES, CREATE_STATUS, UPDATE_STATUS, DELETE_STATUS
from task_manager.labels.constants import \
    LIST_LABELS, CREATE_LABEL, UPDATE_LABEL, DELETE_LABEL
from task_manager.tasks.constants import \
    LIST_TASKS, CREATE_TASK, UPDATE_TASK, DELETE_TASK, DETAIL_TASK


class HomePageTest(TestCase):

    fixtures = ['user.json']

    def test_user_update_view(self) -> None:
        ROUTE = reverse_lazy(HOME)

        response: HttpResponse = self.client.get(ROUTE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name=TEMPLATE_INDEX)


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
            REVERSE_LOGIN, self.credentials, follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, REVERSE_HOME)
        # Should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self) -> None:
        # Log in and make sure the session is valid
        self.client.login(**self.credentials)
        self.assertTrue(SESSION_KEY in self.client.session)
        # There should be no session key on exit
        response: HttpResponse = self.client.get(REVERSE_LOGOUT)
        self.assertTrue(SESSION_KEY not in self.client.session)
        # Checking if a redirect exists
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_HOME)


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
                UPDATE_STATUS, DELETE_STATUS,
                UPDATE_TASK, DELETE_TASK, DETAIL_TASK,
                UPDATE_LABEL, DELETE_LABEL
            )
            without_pk: Tuple[str] = (
                LIST_STATUSES, CREATE_STATUS,
                LIST_TASKS, CREATE_TASK,
                LIST_LABELS, CREATE_LABEL
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
        self.assertRedirects(response, REVERSE_LOGIN)
        self.assertRaisesMessage(
            expected_exception=PermissionDenied,
            expected_message=MSG_NO_PERMISSION
        )

    def test_prohibition_of_changing_user_info_by_another_user(self) -> None:
        inaccessible_id: int = 2  # recall that we are a client with ID 1
        for route in (UPDATE_USER, DELETE_USER):
            response: HttpResponse = self.authenticated_client.get(
                reverse_lazy(route, args=[inaccessible_id])
            )
            self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_unavailability_of_task_deletion_by_non_authors(self) -> None:
        response: HttpResponse = self.authenticated_client.get(
            DELETE_TASK, args=[1]
        )  # the task author must not be the same as the user's client under test

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
