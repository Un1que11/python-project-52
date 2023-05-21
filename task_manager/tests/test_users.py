from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.forms.utils import ErrorDict
from django.core.exceptions import ObjectDoesNotExist

from http import HTTPStatus
from typing import List, Dict

from task_manager.users.models import User
from task_manager.users.constants import UPDATE_USER, DELETE_USER, \
    TEMPLATE_CREATE, TEMPLATE_LIST, TEMPLATE_UPDATE, TEMPLATE_DELETE, \
    REVERSE_USERS, REVERSE_CREATE, REVERSE_LOGIN


class UsersTest(TestCase):

    fixtures = ['user.json']

    VALID_DATA: Dict[str, str] = {
        'username': '@The-Boy+Who_L1ved.',
        'first_name': 'Harry',
        'last_name': 'Potter',
        'password1': 'VeryComplexPassword123',
        'password2': 'VeryComplexPassword123'
    }

    def setUp(self) -> None:
        self.client: Client = Client()
        self.user1: User = User.objects.get(pk=1)
        self.user2: User = User.objects.get(pk=2)
        self.user3: User = User.objects.get(pk=3)

    # DB TESTING

    def assertUser(self, user, user_data) -> None:
        self.assertEqual(user.__str__(), user_data['name'])
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name, user_data['last_name'])

    def test_user_exists(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_USERS)

        users_list: List = list(response.context['users'])
        self.assertTrue(len(users_list) == 3)

        user1, user2, user3 = users_list
        self.assertEqual(user1.username, 'Quidditch-Seeker')
        self.assertEqual(user1.first_name, 'Hary')
        self.assertEqual(user1.last_name, 'Poter')
        self.assertEqual(user2.username, '@Ron_Weas1ey')
        self.assertEqual(user2.first_name, 'Ronald')
        self.assertEqual(user2.last_name, 'Weasley')
        self.assertEqual(user3.username, 'ms.Granger')
        self.assertEqual(user3.first_name, 'Hermione Jean')
        self.assertEqual(user3.last_name, 'Granger')

    def test_user_model_representation(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_USERS)

        users_list: List = list(response.context['users'])

        user1, user2, user3 = users_list
        self.assertEqual(user1.__str__(), 'Hary Poter')
        self.assertEqual(user2.__str__(), 'Ronald Weasley')
        self.assertEqual(user3.__str__(), 'Hermione Jean Granger')

    # LIST VIEW TESTING

    def test_users_list_view(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_USERS)

        self.assertTemplateUsed(response, template_name=TEMPLATE_LIST)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_users_list_view_has_create_link(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_USERS)
        self.assertContains(response, '/users/create/')

    def test_users_list_view_has_update_and_delete_links(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_USERS)
        for user_id in range(1, len(response.context['users']) + 1):
            self.assertContains(response, '/users/{}/update/'.format(user_id))
            self.assertContains(response, '/users/{}/delete/'.format(user_id))

    # CREATE VIEW TESTING & FORM

    def test_user_create_view(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_CREATE)

        self.assertTemplateUsed(response, template_name=TEMPLATE_CREATE)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_create_post_with_validation_errors(self) -> None:
        ROUTE = REVERSE_CREATE

        # Username is required
        params: Dict[str, str] = UsersTest.VALID_DATA.copy()
        params.update({'username': ''})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('username', errors)
        self.assertEqual(
            ['Обязательное поле.'],
            errors['username']
        )

        # Username too long
        params: Dict[str, str] = UsersTest.VALID_DATA.copy()
        params.update({'username': '@The-Boy+Who_L1ved.' * 10})  # len == 190

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('username', errors)
        self.assertEqual(
            ['Убедитесь, что это значение содержит не более 150 символов '
                + '(сейчас {}).'.format(len(params['username']))],
            errors['username']
        )

        # Username contains a space
        params: Dict[str, str] = UsersTest.VALID_DATA.copy()
        params.update({'username': 'The Boy Who Lived'})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('username', errors)
        # ToDo

        # Firstname is required
        params: Dict[str, str] = UsersTest.VALID_DATA.copy()
        params.update({'first_name': ''})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('first_name', errors)
        self.assertEqual(
            ['Обязательное поле.'],
            errors['first_name']
        )

        # Firstname too long
        params: Dict[str, str] = UsersTest.VALID_DATA.copy()
        params.update({'first_name': 'Harry' * 40})  # len == 200

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('first_name', errors)
        self.assertEqual(
            ['Убедитесь, что это значение содержит не более 150 символов '
                + '(сейчас {}).'.format(len(params['first_name']))],
            errors['first_name']
        )

        # Lastname is required
        params: Dict[str, str] = UsersTest.VALID_DATA.copy()
        params.update({'last_name': ''})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('last_name', errors)
        self.assertEqual(
            ['Обязательное поле.'],
            errors['last_name']
        )

        # Lastname too long
        params: Dict[str, str] = UsersTest.VALID_DATA.copy()
        params.update({'last_name': 'Potter' * 30})  # len == 180

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('last_name', errors)
        self.assertEqual(
            ['Убедитесь, что это значение содержит не более 150 символов '
                + '(сейчас {}).'.format(len(params['last_name']))],
            errors['last_name']
        )

    def test_user_create(self) -> None:
        ROUTE = REVERSE_CREATE

        params: Dict[str, str] = UsersTest.VALID_DATA.copy()

        response: HttpResponse = self.client.post(ROUTE, data=params)
        self.assertTrue(User.objects.get(id=4))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_LOGIN)

    # UPDATE VIEW TESTING

    def test_user_update_view(self) -> None:
        ROUTE = reverse_lazy(UPDATE_USER, args=[self.user1.id])

        self.client.force_login(self.user1)
        response: HttpResponse = self.client.get(ROUTE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name=TEMPLATE_UPDATE)

    def test_user_update(self) -> None:
        ROUTE = reverse_lazy(UPDATE_USER, args=[self.user1.id])

        original_objs_count: int = len(User.objects.all())
        params: Dict[str, str] = UsersTest.VALID_DATA
        params.update({'email': 'harry_potter@hogwarts.mail'})

        self.client.force_login(self.user1)
        response: HttpResponse = self.client.post(ROUTE, data=params)
        final_objs_count: int = len(User.objects.all())
        self.assertTrue(final_objs_count == original_objs_count)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_USERS)

        updated_user: User = User.objects.get(id=self.user1.id)
        self.assertEqual(updated_user.username, params['username'])
        self.assertEqual(updated_user.first_name, params['first_name'])
        self.assertEqual(updated_user.last_name, params['last_name'])
        self.assertEqual(updated_user.email, params['email'])

    # DELETE VIEW TESTING

    def test_user_delete_view(self) -> None:
        ROUTE = reverse_lazy(DELETE_USER, args=[self.user1.id])

        self.client.force_login(self.user1)
        response: HttpResponse = self.client.get(ROUTE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name=TEMPLATE_DELETE)

    def test_user_delete(self) -> None:
        ROUTE = reverse_lazy(DELETE_USER, args=[self.user1.id])

        original_objs_count: int = len(User.objects.all())

        self.client.force_login(self.user1)
        response: HttpResponse = self.client.post(ROUTE)
        final_objs_count: int = len(User.objects.all())
        self.assertTrue(final_objs_count == original_objs_count - 1)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_USERS)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(id=self.user1.id)
