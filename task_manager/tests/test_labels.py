from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.forms.utils import ErrorDict
from django.core.exceptions import ObjectDoesNotExist

from http import HTTPStatus
from typing import List, Dict

from task_manager.labels.models import Label
from task_manager.users.models import User
from task_manager.labels.constants import \
    TEMPLATE_CREATE, TEMPLATE_LIST, TEMPLATE_UPDATE, TEMPLATE_DELETE, \
    REVERSE_LABELS, REVERSE_CREATE, UPDATE_LABEL, DELETE_LABEL


class LabelsTest(TestCase):

    fixtures = ['label.json', 'user.json']

    VALID_DATA: Dict[str, str] = {'name': 'Task Manager'}

    def setUp(self) -> None:
        self.client: Client = Client()
        self.client.force_login(User.objects.get(pk=1))
        self.label1: Label = Label.objects.get(pk=1)
        self.label2: Label = Label.objects.get(pk=2)
        self.label3: Label = Label.objects.get(pk=3)

    # DB TESTING

    def assertLabel(self, label, label_data) -> None:
        self.assertEqual(label.__str__(), label_data['name'])
        self.assertEqual(label.name, label_data['name'])

    def test_label_exists(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_LABELS)

        labels_list: List = list(response.context['labels'])
        self.assertTrue(len(labels_list) == 3)

        label1, label2, label3 = labels_list
        self.assertEqual(label1.name, 'Development')
        self.assertEqual(label2.name, 'Testing')
        self.assertEqual(label3.name, 'Optimization')

    def test_label_model_representation(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_LABELS)

        labels_list: List = list(response.context['labels'])

        label1, label2, label3 = labels_list
        self.assertEqual(label1.__str__(), 'Development')
        self.assertEqual(label2.__str__(), 'Testing')
        self.assertEqual(label3.__str__(), 'Optimization')

    # LIST VIEW TESTING

    def test_labels_list_view(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_LABELS)

        self.assertTemplateUsed(response, template_name=TEMPLATE_LIST)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_labels_list_view_has_create_link(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_LABELS)
        self.assertContains(response, '/labels/create/')

    def test_labels_list_view_has_update_and_delete_links(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_LABELS)
        for label_id in range(1, len(response.context['labels']) + 1):
            self.assertContains(response, '/labels/{}/update/'.format(label_id))
            self.assertContains(response, '/labels/{}/delete/'.format(label_id))

    # CREATE VIEW TESTING & FORM

    def test_label_create_view(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_CREATE)

        self.assertTemplateUsed(response, template_name=TEMPLATE_CREATE)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_label_create_post_with_validation_errors(self) -> None:
        ROUTE = REVERSE_CREATE

        # Label name is required
        params: Dict[str, str] = LabelsTest.VALID_DATA.copy()
        params.update({'name': ''})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('name', errors)
        self.assertEqual(
            ['Обязательное поле.'],
            errors['name']
        )

        # Label name too long
        params: Dict[str, str] = LabelsTest.VALID_DATA.copy()
        params.update({'name': '*' * 101})  # len == 101

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('name', errors)
        self.assertEqual(
            ['Убедитесь, что это значение содержит не более 100 символов '
                + '(сейчас {}).'.format(len(params['name']))],
            errors['name']
        )

    def test_label_create(self) -> None:
        ROUTE = REVERSE_CREATE

        params: Dict[str, str] = LabelsTest.VALID_DATA.copy()

        response: HttpResponse = self.client.post(ROUTE, data=params)
        self.assertTrue(Label.objects.get(id=4))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_LABELS)

    # UPDATE VIEW TESTING

    def test_label_update_view(self) -> None:
        ROUTE = reverse_lazy(UPDATE_LABEL, args=[self.label1.id])

        response: HttpResponse = self.client.get(ROUTE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name=TEMPLATE_UPDATE)

    def test_label_update(self) -> None:
        ROUTE = reverse_lazy(UPDATE_LABEL, args=[self.label1.id])

        original_objs_count: int = len(Label.objects.all())
        params: Dict[str, str] = LabelsTest.VALID_DATA
        params.update({'name': 'updated label name'})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        final_objs_count: int = len(Label.objects.all())
        self.assertTrue(final_objs_count == original_objs_count)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_LABELS)

        updated_label: Label = Label.objects.get(id=self.label1.id)
        self.assertEqual(updated_label.name, params['name'])

    # DELETE VIEW TESTING

    def test_label_delete_view(self) -> None:
        ROUTE = reverse_lazy(DELETE_LABEL, args=[self.label1.id])

        response: HttpResponse = self.client.get(ROUTE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name=TEMPLATE_DELETE)

    def test_label_delete(self) -> None:
        ROUTE = reverse_lazy(DELETE_LABEL, args=[self.label1.id])

        original_objs_count: int = len(Label.objects.all())

        response: HttpResponse = self.client.post(ROUTE)
        final_objs_count: int = len(Label.objects.all())
        self.assertTrue(final_objs_count == original_objs_count - 1)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_LABELS)
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=self.label1.id)
