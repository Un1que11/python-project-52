from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.forms.utils import ErrorDict
from django.core.exceptions import ObjectDoesNotExist

from http import HTTPStatus
from typing import List, Dict

from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.statuses.constants import \
    TEMPLATE_CREATE, TEMPLATE_LIST, TEMPLATE_UPDATE, TEMPLATE_DELETE, \
    REVERSE_STATUSES, REVERSE_CREATE, UPDATE_STATUS, DELETE_STATUS


class StatusesTest(TestCase):

    fixtures = ['status.json', 'user.json']

    VALID_DATA: Dict[str, str] = {'name': 'On testing'}

    def setUp(self) -> None:
        self.client: Client = Client()
        self.client.force_login(User.objects.get(pk=1))
        self.status1: Status = Status.objects.get(pk=1)
        self.status2: Status = Status.objects.get(pk=2)
        self.status3: Status = Status.objects.get(pk=3)

    # DB TESTING

    def assertStatus(self, status, status_data) -> None:
        self.assertEqual(status.__str__(), status_data['name'])
        self.assertEqual(status.name, status_data['name'])

    def test_status_exists(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_STATUSES)

        statuses_list: List = list(response.context['statuses'])
        self.assertTrue(len(statuses_list) == 3)

        status1, status2, status3 = statuses_list
        self.assertEqual(status1.name, 'New')
        self.assertEqual(status2.name, 'In progress')
        self.assertEqual(status3.name, 'Completed')

    def test_status_model_representation(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_STATUSES)

        statuses_list: List = list(response.context['statuses'])

        status1, status2, status3 = statuses_list
        self.assertEqual(status1.__str__(), 'New')
        self.assertEqual(status2.__str__(), 'In progress')
        self.assertEqual(status3.__str__(), 'Completed')

    # LIST VIEW TESTING

    def test_statuses_list_view(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_STATUSES)

        self.assertTemplateUsed(response, template_name=TEMPLATE_LIST)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_statuses_list_view_has_create_link(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_STATUSES)
        self.assertContains(response, '/statuses/create/')

    def test_statuses_list_view_has_update_and_delete_links(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_STATUSES)
        for status_id in range(1, len(response.context['statuses']) + 1):
            self.assertContains(response, '/statuses/{}/update/'.format(status_id))
            self.assertContains(response, '/statuses/{}/delete/'.format(status_id))

    # CREATE VIEW TESTING & FORM

    def test_status_create_view(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_CREATE)

        self.assertTemplateUsed(response, template_name=TEMPLATE_CREATE)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_status_create_post_with_validation_errors(self) -> None:
        ROUTE = REVERSE_CREATE

        # Status name is required
        params: Dict[str, str] = StatusesTest.VALID_DATA.copy()
        params.update({'name': ''})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('name', errors)
        self.assertEqual(
            ['Обязательное поле.'],
            errors['name']
        )

        # Status name too long
        params: Dict[str, str] = StatusesTest.VALID_DATA.copy()
        params.update({'name': '*' * 41})  # len == 41

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('name', errors)
        self.assertEqual(
            ['Убедитесь, что это значение содержит не более 40 символов '
                + '(сейчас {}).'.format(len(params['name']))],
            errors['name']
        )

    def test_status_create(self) -> None:
        ROUTE = REVERSE_CREATE

        params: Dict[str, str] = StatusesTest.VALID_DATA.copy()

        response: HttpResponse = self.client.post(ROUTE, data=params)
        self.assertTrue(Status.objects.get(id=4))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_STATUSES)

    # UPDATE VIEW TESTING

    def test_status_update_view(self) -> None:
        ROUTE = reverse_lazy(UPDATE_STATUS, args=[self.status1.id])

        response: HttpResponse = self.client.get(ROUTE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name=TEMPLATE_UPDATE)

    def test_status_update(self) -> None:
        ROUTE = reverse_lazy(UPDATE_STATUS, args=[self.status1.id])

        original_objs_count: int = len(Status.objects.all())
        params: Dict[str, str] = StatusesTest.VALID_DATA
        params.update({'name': 'updated status name'})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        final_objs_count: int = len(Status.objects.all())
        self.assertTrue(final_objs_count == original_objs_count)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_STATUSES)

        updated_status: Status = Status.objects.get(id=self.status1.id)
        self.assertEqual(updated_status.name, params['name'])

    # DELETE VIEW TESTING

    def test_status_delete_view(self) -> None:
        ROUTE = reverse_lazy(DELETE_STATUS, args=[self.status1.id])

        response: HttpResponse = self.client.get(ROUTE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name=TEMPLATE_DELETE)

    def test_status_delete(self) -> None:
        ROUTE = reverse_lazy(DELETE_STATUS, args=[self.status1.id])

        original_objs_count: int = len(Status.objects.all())

        response: HttpResponse = self.client.post(ROUTE)
        final_objs_count: int = len(Status.objects.all())
        self.assertTrue(final_objs_count == original_objs_count - 1)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_STATUSES)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=self.status1.id)
