from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from typing import Dict, Tuple, Type

from .models import Status
from ..mixins import AuthorizationPermissionMixin, DeletionProtectionMixin


class StatusesListView(AuthorizationPermissionMixin, ListView):
    '''Show the list of statuses.'''
    model: Type[Status] = Status
    context_object_name: str = 'statuses'
    extra_context: Dict = {
            'page_title': _('Statuses'),
            'page_description': _('List of Task Manager Statuses.'),
            'page_h1': _('Statuses')
            }


class StatusCreateView(AuthorizationPermissionMixin,
                       SuccessMessageMixin, CreateView):
    '''Create a status.'''
    model: Type[Status] = Status
    extra_context: Dict = {
            'page_title': _('Status creation'),
            'page_description': _('Status Creation on Task Manager.'),
            'page_h1': _('Create status'),
            'button_text': _('Create')
            }
    fields: Tuple = ('name',)
    success_url = reverse_lazy('statuses')
    success_message: str = _('Status created successfully')


class StatusUpdateView(AuthorizationPermissionMixin,
                       SuccessMessageMixin, UpdateView):
    '''Change a status.'''
    model: Type[Status] = Status
    extra_context: Dict = {
            'page_title': _('Status editing'),
            'page_description': _('Status editing on Task Manager.'),
            'page_h1': _('Change Status'),
            'button_text': _('Update')
            }
    fields: Tuple = ('name',)
    success_url = reverse_lazy('statuses')
    success_message: str = _('Status changed successfully')


class StatusDeleteView(AuthorizationPermissionMixin,
                       DeletionProtectionMixin, SuccessMessageMixin, DeleteView):
    '''Delete a status.'''
    model: Type[Status] = Status
    extra_context: Dict = {
            'page_title': _('Status deleting'),
            'page_description': _('Status deleting on Task Manager.'),
            'page_h1': _('Delete status'),
            'button_text': _('Yes, delete')
            }
    context_object_name: str = 'status'
    success_url = reverse_lazy('statuses')
    success_message: str = _('Status deleted successfully')
    protected_data_url = reverse_lazy('statuses')
    protected_data_message: str = _('Can\'t delete status because it\'s in use')
