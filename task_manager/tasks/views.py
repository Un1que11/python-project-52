from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.forms.forms import BaseForm
from django.http import HttpResponse
from typing import Dict, Tuple, Type

from django_filters.views import FilterView

from .filters import TasksFilter
from .models import Task, User
from ..mixins import AuthorizationPermissionMixin


class TasksListView(AuthorizationPermissionMixin, FilterView):
    '''Show the list of tasks.'''
    model: Type[Task] = Task
    context_object_name: str = 'tasks'
    extra_context: Dict = {
        'page_title': _('Tasks'),
        'page_description': _('Liste of Task Manager Tasks.'),
        'page_h1': _('Tasks'),
        'button_text': _('Search')
    }
    filterset_class: Type[TasksFilter] = TasksFilter


class TaskCreateView(AuthorizationPermissionMixin,
                     SuccessMessageMixin, CreateView):
    '''Create a task.'''
    model: Type[Task] = Task
    extra_context: Dict = {
        'page_title': _('Task creation'),
        'page_description': _('Task Creation on Task Manager.'),
        'page_h1': _('Create task'),
        'button_text': _('Create')
    }
    fields: Tuple = ('name', 'status', 'description', 'executor', 'labels')
    success_url = reverse_lazy('tasks')
    success_message: str = _('Task created successfully')

    def form_valid(self, form: BaseForm) -> HttpResponse:
        '''Sets the author of the task by the ID of the current user.'''
        user: User = self.request.user
        form.instance.author: BaseForm[User] = User.objects.get(id=user.id)
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(AuthorizationPermissionMixin,
                     SuccessMessageMixin, UpdateView):
    '''Change a task.'''
    model: Type[Task] = Task
    extra_context: Dict = {
        'page_title': _('Task editing'),
        'page_description': _('Task editing on Task Manager.'),
        'page_h1': _('Change task'),
        'button_text': _('Update')
    }
    fields: Tuple = ('name', 'status', 'description', 'executor', 'labels')
    success_url = reverse_lazy('tasks')
    success_message: str = _('Task changed successfully')


class TaskDeleteView(AuthorizationPermissionMixin,
                     SuccessMessageMixin, DeleteView):
    '''Delete a task.'''
    model: Type[Task] = Task
    context_object_name: str = 'task'
    extra_context: Dict = {
        'page_title': _('Task deleting'),
        'page_description': _('Task deleting on Task Manager.'),
        'page_h1': _('Delete task'),
        'button_text': _('Yes, delete')
    }
    success_url = reverse_lazy('tasks')
    success_message: str = _('Task deleted successfully')

    def dispatch(self, request, *args, **kwargs):
        '''Specifies access settings for the current user.
        Provides access if the user is authenticated.'''
        if request.user.id != self.get_object().author.id:
            if request.user.is_authenticated:
                messages.error(self.request, _('A task can only be deleted by its author.'))
            return redirect(reverse_lazy('tasks'))
        return super().dispatch(request, *args, **kwargs)


class TaskDetailView(AuthorizationPermissionMixin, DetailView):
    model: Type[Task] = Task
    extra_context: Dict = {
        'page_title': _('Task view'),
        'page_description': _('Task detail view on Task Manager.'),
        'page_h1': _('Task view')
    }
