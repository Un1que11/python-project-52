from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from typing import Dict, Tuple, Type

from .models import Label
from ..mixins import AuthorizationPermissionMixin, DeletionProtectionMixin


class LabelsListView(AuthorizationPermissionMixin, ListView):
    '''Show the list of labels.'''
    model: Type[Label] = Label
    context_object_name: str = 'labels'
    extra_context: Dict = {
            'page_title': _('Labels'),
            'page_description': _('List of Task Manager Labels.'),
            'page_h1': _('Labels')
    }


class LabelCreateView(AuthorizationPermissionMixin,
                      SuccessMessageMixin, CreateView):
    '''Create a label.'''
    model: Type[Label] = Label
    extra_context: Dict = {
            'page_title': _('Label creation'),
            'page_description': _('Label Creation on Task Manager.'),
            'page_h1': _('Create label'),
            'button_text': _('Create')
    }
    fields: Tuple = ('name',)
    success_url = reverse_lazy('labels')
    success_message: str = _('Label created successfully')


class LabelUpdateView(AuthorizationPermissionMixin,
                      SuccessMessageMixin, UpdateView):
    '''Change a label.'''
    model: Type[Label] = Label
    extra_context: Dict = {
            'page_title': _('Label editing'),
            'page_description': _('Label editing on Task Manager.'),
            'page_h1': _('Change label'),
            'button_text': _('Update')
    }
    fields: Tuple = ('name',)
    success_url = reverse_lazy('labels')
    success_message: str = _('Label changed successfully')


class LabelDeleteView(AuthorizationPermissionMixin,
                      DeletionProtectionMixin, SuccessMessageMixin, DeleteView):
    '''Delete a label.'''
    model: Type[Label] = Label
    context_object_name: str = 'label'
    extra_context: Dict = {
            'page_title': _('Label deleting'),
            'page_description': _('Label deleting on Task Manager.'),
            'page_h1': _('Delete label'),
            'button_text': _('Yes, delete')
    }
    success_url = reverse_lazy('labels')
    success_message: str = _('Label deleted successfully')
    protected_data_url = reverse_lazy('labels')
    protected_data_message: str = _('Can\'t delete label because it\'s in use')
