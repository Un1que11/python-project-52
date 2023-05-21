from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.forms.forms import BaseForm
from django.http import HttpResponse
from typing import Dict, Any, Tuple, Union, Callable, Type

from django_filters.views import FilterView

from .filters import TasksFilter
from .models import Task, User
from .constants import REVERSE_TASKS, \
    CONTEXT_LIST, CONTEXT_CREATE, CONTEXT_UPDATE, CONTEXT_DELETE, CONTEXT_DETAIL, \
    MSG_CREATED, MSG_UPDATED, MSG_DELETED, MSG_NOT_AUTHOR_FOR_DELETE_TASK, \
    NAME, STATUS, DESCRIPTION, EXECUTOR, LABELS
from ..mixins import AuthorizationPermissionMixin


class TasksListView(AuthorizationPermissionMixin, FilterView):
    '''Show the list of tasks.'''
    model: Type[Task] = Task
    context_object_name: str = 'tasks'
    extra_context: Dict = CONTEXT_LIST
    filterset_class: Type[TasksFilter] = TasksFilter


class TaskCreateView(AuthorizationPermissionMixin,
                     SuccessMessageMixin, CreateView):
    '''Create a task.'''
    model: Type[Task] = Task
    extra_context: Dict = CONTEXT_CREATE
    fields: Tuple = (NAME, STATUS, DESCRIPTION, EXECUTOR, LABELS)
    success_url: Union[str, Callable[..., Any]] = REVERSE_TASKS
    success_message: str = MSG_CREATED

    def form_valid(self, form: BaseForm) -> HttpResponse:
        '''Sets the author of the task by the ID of the current user.'''
        user: User = self.request.user
        form.instance.author: BaseForm[User] = User.objects.get(id=user.id)
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(AuthorizationPermissionMixin,
                     SuccessMessageMixin, UpdateView):
    '''Change a task.'''
    model: Type[Task] = Task
    extra_context: Dict = CONTEXT_UPDATE
    fields: Tuple = (NAME, STATUS, DESCRIPTION, EXECUTOR, LABELS)
    success_url: Union[str, Callable[..., Any]] = REVERSE_TASKS
    success_message: str = MSG_UPDATED


class TaskDeleteView(AuthorizationPermissionMixin,
                     SuccessMessageMixin, DeleteView):
    '''Delete a task.'''
    model: Type[Task] = Task
    context_object_name: str = 'task'
    extra_context: Dict = CONTEXT_DELETE
    success_url: Union[str, Callable[..., Any]] = REVERSE_TASKS
    success_message: str = MSG_DELETED

    def dispatch(self, request, *args, **kwargs):
        '''Specifies access settings for the current user.
        Provides access if the user is authenticated.'''
        if request.user.id != self.get_object().author.id:
            if request.user.is_authenticated:
                messages.error(self.request, MSG_NOT_AUTHOR_FOR_DELETE_TASK)
            return redirect(REVERSE_TASKS)
        return super().dispatch(request, *args, **kwargs)


class TaskDetailView(AuthorizationPermissionMixin, DetailView):
    model: Type[Task] = Task
    extra_context: Dict = CONTEXT_DETAIL
