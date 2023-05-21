from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.forms.utils import ErrorDict
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from http import HTTPStatus
from typing import List, Dict

from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.models import User
from task_manager.tasks.constants import \
    TEMPLATE_CREATE, TEMPLATE_LIST, TEMPLATE_UPDATE, TEMPLATE_DELETE, TEMPLATE_DETAIL, \
    REVERSE_TASKS, REVERSE_CREATE, UPDATE_TASK, DELETE_TASK, DETAIL_TASK, \
    MSG_NOT_AUTHOR_FOR_DELETE_TASK
from task_manager.statuses.constants import \
    REVERSE_STATUSES, DELETE_STATUS, STATUS_USED_IN_TASK
from task_manager.labels.constants import \
    REVERSE_LABELS, DELETE_LABEL, LABEL_USED_IN_TASK
from task_manager.users.constants import \
    REVERSE_USERS, DELETE_USER, USER_USED_IN_TASK


class TasksTest(TestCase):

    fixtures = ['task.json', 'label.json', 'status.json', 'user.json']

    VALID_DATA: Dict[str, str] = {
        'name': 'Task name',
        'status': 1,
        'description': 'Task description',
        'executor': 2,
    }

    def setUp(self) -> None:
        self.client: Client = Client()
        self.client.force_login(User.objects.get(pk=1))
        self.task1: Task = Task.objects.get(pk=1)
        self.task2: Task = Task.objects.get(pk=2)
        self.task3: Task = Task.objects.get(pk=3)

        self.user1: User = User.objects.get(pk=1)
        self.user2: User = User.objects.get(pk=2)
        self.user3: User = User.objects.get(pk=3)

        self.status1: Status = Status.objects.get(pk=1)
        self.status2: Status = Status.objects.get(pk=2)
        self.status3: Status = Status.objects.get(pk=3)

    # DB TESTING

    def assertTask(self, task, task_data) -> None:
        self.assertEqual(task.__str__(), task_data['name'])
        self.assertEqual(task.name, task_data['name'])
        self.assertEqual(task.status, task_data['status'])
        self.assertEqual(task.description, task_data['description'])
        self.assertEqual(task.author, task_data['author'])
        self.assertEqual(task.executor, task_data['executor'])
        self.assertEqual(task.date_created, task_data['date_created'])
        self.assertEqual(task.date_modified, task_data['date_modified'])

    def test_task_exists(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_TASKS)

        tasks_list: List = list(response.context['tasks'])
        self.assertTrue(len(tasks_list) == 3)

        task1, task2, task3 = tasks_list

        self.assertEqual(task1.name, 'Get Terms of Reference')
        self.assertEqual(task1.status, self.status3)
        self.assertEqual(task1.author, self.user1)
        self.assertEqual(task1.executor, self.user2)
        self.assertEqual(
            task1.description,
            'Get cloud disk access from Galya and open the document.'
        )

        self.assertEqual(task2.name, 'Implement functionality')
        self.assertEqual(task2.status, self.status1)
        self.assertEqual(task2.author, self.user1)
        self.assertEqual(task2.executor, self.user2)
        self.assertEqual(
            task2.description,
            'Write the best and cleanest application code.'
        )

        self.assertEqual(task3.name, 'Hand over the work to the customer')
        self.assertEqual(task3.status, self.status1)
        self.assertEqual(task3.author, self.user2)
        self.assertEqual(task3.executor, self.user1)
        self.assertEqual(
            task3.description,
            'Upload the archive with the code to the cloud drive and give access to Galya.'
        )

    def test_task_model_representation(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_TASKS)

        tasks_list: List = list(response.context['tasks'])

        task1, task2, task3 = tasks_list
        self.assertEqual(task1.__str__(), 'Get Terms of Reference')
        self.assertEqual(task2.__str__(), 'Implement functionality')
        self.assertEqual(task3.__str__(), 'Hand over the work to the customer')

    # LIST VIEW TESTING & TASKS FILTERING

    def test_tasks_list_view(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_TASKS)

        self.assertTemplateUsed(response, template_name=TEMPLATE_LIST)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tasks_list_view_has_create_link(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_TASKS)
        self.assertContains(response, '/tasks/create/')

    def test_tasks_list_view_has_update_and_delete_links(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_TASKS)
        for task_id in range(1, len(response.context['tasks']) + 1):
            self.assertContains(response, '/tasks/{}/update/'.format(task_id))
            self.assertContains(response, '/tasks/{}/delete/'.format(task_id))

    def test_filter_tasks_by_status(self) -> None:
        # Отфильтровать задачи со статусом "New"
        response: HttpResponse = self.client.get(REVERSE_TASKS, {'status': self.status1.pk})
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 2)
        self.assertIn(self.task2, tasks)
        self.assertIn(self.task3, tasks)
        self.assertNotIn(self.task1, tasks)

    def test_filter_tasks_by_executor(self) -> None:
        # Отфильтровать задачи, выполняемые пользователем 2
        response: HttpResponse = self.client.get(REVERSE_TASKS, {'executor': self.user2.pk})
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 2)
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)
        self.assertNotIn(self.task3, tasks)

    def test_filter_tasks_by_labels(self) -> None:
        # Отфильтровать задачи с меткой "Development"
        label = Label.objects.get(name='Development')
        response: HttpResponse = self.client.get(REVERSE_TASKS, {'labels': label.pk})
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 2)
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)
        self.assertNotIn(self.task3, tasks)

    def test_filter_tasks_by_current_user(self) -> None:
        # Отфильтровать задачи текущего пользователя (определен в "setUp")
        response: HttpResponse = self.client.get(REVERSE_TASKS, {'self_tasks': 'on'})
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 2)
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)
        self.assertNotIn(self.task3, tasks)

    # CREATE VIEW TESTING & FORM

    def test_task_create_view(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_CREATE)

        self.assertTemplateUsed(response, template_name=TEMPLATE_CREATE)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_task_create_post_with_validation_errors(self) -> None:
        ROUTE = REVERSE_CREATE

        # Task name is required
        params: Dict[str, str] = TasksTest.VALID_DATA.copy()
        params.update({'name': ''})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('name', errors)
        self.assertEqual(
            ['Обязательное поле.'],
            errors['name']
        )

        # Task name too long
        params: Dict[str, str] = TasksTest.VALID_DATA.copy()
        params.update({'name': '*' * 51})  # len == 51

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('name', errors)
        self.assertEqual(
            ['Убедитесь, что это значение содержит не более 50 символов '
                + '(сейчас {}).'.format(len(params['name']))],
            errors['name']
        )

        # Status is required
        params: Dict[str, str] = TasksTest.VALID_DATA.copy()
        params.update({'status': ''})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('status', errors)
        self.assertEqual(
            ['Обязательное поле.'],
            errors['status']
        )

        # Status does not exist
        params: Dict[str, str] = TasksTest.VALID_DATA.copy()
        params.update({'status': 10})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('status', errors)
        self.assertEqual(
            ['Выберите корректный вариант. Вашего варианта нет среди допустимых значений.'],
            errors['status']
        )

        # Description name is required
        params: Dict[str, str] = TasksTest.VALID_DATA.copy()
        params.update({'description': ''})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('description', errors)
        self.assertEqual(
            ['Обязательное поле.'],
            errors['description']
        )

        # Description too long
        params: Dict[str, str] = TasksTest.VALID_DATA.copy()
        params.update({'description': '*' * 5001})  # len == 5001

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('description', errors)
        self.assertEqual(
            ['Убедитесь, что это значение содержит не более 5000 символов '
                + '(сейчас {}).'.format(len(params['description']))],
            errors['description']
        )

        # Executor does not exist
        params: Dict[str, str] = TasksTest.VALID_DATA.copy()
        params.update({'executor': 10})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        errors: ErrorDict = response.context['form'].errors
        self.assertIn('executor', errors)
        self.assertEqual(
            ['Выберите корректный вариант. Вашего варианта нет среди допустимых значений.'],
            errors['executor']
        )

    def test_task_create(self) -> None:
        ROUTE = REVERSE_CREATE

        params: Dict[str, str] = TasksTest.VALID_DATA.copy()

        response: HttpResponse = self.client.post(ROUTE, data=params)
        self.assertTrue(Task.objects.get(id=4))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_TASKS)

    # UPDATE VIEW TESTING

    def test_task_update_view(self) -> None:
        ROUTE = reverse_lazy(UPDATE_TASK, args=[self.task1.id])

        response: HttpResponse = self.client.get(ROUTE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name=TEMPLATE_UPDATE)

    def test_task_update(self) -> None:
        ROUTE = reverse_lazy(UPDATE_TASK, args=[self.task1.id])

        original_objs_count: int = len(Task.objects.all())
        params: Dict[str, str] = TasksTest.VALID_DATA
        params.update({'name': 'updated task name'})

        response: HttpResponse = self.client.post(ROUTE, data=params)
        final_objs_count: int = len(Task.objects.all())
        self.assertTrue(final_objs_count == original_objs_count)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_TASKS)

        updated_task: Task = Task.objects.get(id=self.task1.id)
        self.assertEqual(updated_task.name, params['name'])

    # DELETE VIEW TESTING

    def test_task_delete_view(self) -> None:
        ROUTE = reverse_lazy(DELETE_TASK, args=[self.task1.id])

        response: HttpResponse = self.client.get(ROUTE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name=TEMPLATE_DELETE)

    def test_task_delete(self) -> None:
        self.client.force_login(self.user2)  # User 2 is Task 3 author
        ROUTE = reverse_lazy(DELETE_TASK, args=[self.task3.id])

        original_objs_count: int = len(Task.objects.all())
        response: HttpResponse = self.client.post(ROUTE, follow=True)
        final_objs_count: int = len(Task.objects.all())

        self.assertTrue(final_objs_count == original_objs_count - 1)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, REVERSE_TASKS)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=self.task3.id)

    def test_not_self_task_delete(self) -> None:
        ROUTE = reverse_lazy(DELETE_TASK, args=[self.task3.id])
        original_objs_count: int = len(Task.objects.all())
        # GET
        get_response: HttpResponse = self.client.get(ROUTE)
        final_objs_count: int = len(Task.objects.all())
        self.assertTrue(final_objs_count == original_objs_count)
        self.assertRedirects(get_response, REVERSE_TASKS)
        self.assertEqual(len(Task.objects.all()), 3)
        self.assertRaisesMessage(
            expected_exception=PermissionDenied,
            expected_message=MSG_NOT_AUTHOR_FOR_DELETE_TASK
        )
        # POST
        post_response: HttpResponse = self.client.post(ROUTE)
        final_objs_count: int = len(Task.objects.all())
        self.assertTrue(final_objs_count == original_objs_count)
        self.assertRedirects(post_response, REVERSE_TASKS)
        self.assertEqual(len(Task.objects.all()), 3)
        self.assertRaisesMessage(
            expected_exception=PermissionDenied,
            expected_message=MSG_NOT_AUTHOR_FOR_DELETE_TASK
        )

    # DETAIL VIEW TESTING

    def test_task_detail_view(self) -> None:
        ROUTE = reverse_lazy(DETAIL_TASK, args=[3])

        response: HttpResponse = self.client.get(ROUTE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name=TEMPLATE_DETAIL)


class TestDeleteRelatedEntities(TestCase):

    fixtures = ['task.json', 'label.json', 'status.json', 'user.json']

    def setUp(self) -> None:
        self.client: Client = Client()
        self.client.force_login(User.objects.get(pk=1))
        self.task1: Task = Task.objects.get(pk=1)
        self.task2: Task = Task.objects.get(pk=2)
        self.task3: Task = Task.objects.get(pk=3)

        self.user1: User = User.objects.get(pk=1)
        self.user2: User = User.objects.get(pk=2)
        self.user3: User = User.objects.get(pk=3)

        self.status1: Status = Status.objects.get(pk=1)
        self.status2: Status = Status.objects.get(pk=2)
        self.status3: Status = Status.objects.get(pk=3)

        self.label1: Label = Label.objects.get(pk=1)
        self.label2: Label = Label.objects.get(pk=2)
        self.label3: Label = Label.objects.get(pk=3)

    # STATUS

    def test_delete_status(self):
        # отправляем запрос на удаление связанного с задачей статуса
        response: HttpResponse = self.client.post(
            reverse_lazy(DELETE_STATUS, args=[self.status1.id]), follow=True
        )
        self.assertEqual(Status.objects.count(), 3)
        # проверяем, что получен ответ с кодом 200, т.к. обрабатываем ProtectedError
        self.assertRedirects(response, REVERSE_STATUSES)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message=STATUS_USED_IN_TASK
        )

    def test_delete_unused_status(self):
        # отправляем запрос на удаление не связанного с задачей статуса
        response: HttpResponse = self.client.post(
            reverse_lazy(DELETE_STATUS, args=[self.status2.id]), follow=True
        )
        self.assertEqual(Status.objects.count(), 2)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # AUTHOR

    def test_delete_author(self):
        # отправляем запрос на удаление автора задачи
        response: HttpResponse = self.client.post(
            reverse_lazy(DELETE_USER, args=[self.user1.id]), follow=True
        )
        self.assertEqual(User.objects.count(), 3)
        # проверяем, что получен ответ с кодом 200, т.к. обрабатываем ProtectedError
        self.assertRedirects(response, REVERSE_USERS)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message=USER_USED_IN_TASK
        )

    def test_delete_unused_author(self):
        # отправляем запрос на удаление пользователя задачи без авторских прав
        self.client.force_login(self.user3)
        response: HttpResponse = self.client.post(
            reverse_lazy(DELETE_USER, args=[self.user3.id]), follow=True
        )
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # EXECUTOR

    def test_delete_executor(self):
        # отправляем запрос на удаление исполнителя задачи
        response: HttpResponse = self.client.post(
            reverse_lazy(DELETE_USER, args=[self.user1.id]), follow=True
        )
        self.assertEqual(User.objects.count(), 3)
        # проверяем, что получен ответ с кодом 200, т.к. обрабатываем ProtectedError
        self.assertRedirects(response, REVERSE_USERS)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message=USER_USED_IN_TASK
        )

    def test_delete_unused_executor(self):
        # отправляем запрос на удаление пользователя без исполнительных обязанностей
        self.client.force_login(self.user3)
        response: HttpResponse = self.client.post(
            reverse_lazy(DELETE_USER, args=[self.user3.id]), follow=True
        )
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # LABEL

    def test_delete_label(self):
        # отправляем запрос на удаление связанной с задачей метки
        response: HttpResponse = self.client.post(
            reverse_lazy(DELETE_LABEL, args=[self.label1.id]), follow=True
        )
        self.assertEqual(Label.objects.count(), 3)
        # проверяем, что получен ответ с кодом 200, т.к. обрабатываем ProtectedError
        self.assertRedirects(response, REVERSE_LABELS)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message=LABEL_USED_IN_TASK
        )

    def test_delete_unused_label(self):
        # отправляем запрос на удаление не связанной с задачей метки
        response: HttpResponse = self.client.post(
            reverse_lazy(DELETE_LABEL, args=[self.label2.id]), follow=True
        )
        self.assertEqual(Label.objects.count(), 2)
        self.assertEqual(response.status_code, HTTPStatus.OK)
