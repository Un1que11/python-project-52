from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from typing import Dict, Any, Tuple, Union, Callable, Type

from .models import Label
from .constants import REVERSE_LABELS, NAME, \
    CONTEXT_LIST, CONTEXT_CREATE, CONTEXT_UPDATE, CONTEXT_DELETE, \
    MSG_CREATED, MSG_UPDATED, MSG_DELETED, LABEL_USED_IN_TASK
from ..mixins import AuthorizationPermissionMixin, DeletionProtectionMixin


class LabelsListView(AuthorizationPermissionMixin, ListView):
    '''Show the list of labels.'''
    model: Type[Label] = Label
    context_object_name: str = 'labels'
    extra_context: Dict = CONTEXT_LIST


class LabelCreateView(AuthorizationPermissionMixin,
                      SuccessMessageMixin, CreateView):
    '''Create a label.'''
    model: Type[Label] = Label
    extra_context: Dict = CONTEXT_CREATE
    fields: Tuple = (NAME,)
    success_url: Union[str, Callable[..., Any]] = REVERSE_LABELS
    success_message: str = MSG_CREATED


class LabelUpdateView(AuthorizationPermissionMixin,
                      SuccessMessageMixin, UpdateView):
    '''Change a label.'''
    model: Type[Label] = Label
    extra_context: Dict = CONTEXT_UPDATE
    fields: Tuple = (NAME,)
    success_url: Union[str, Callable[..., Any]] = REVERSE_LABELS
    success_message: str = MSG_UPDATED


class LabelDeleteView(AuthorizationPermissionMixin,
                      DeletionProtectionMixin, SuccessMessageMixin, DeleteView):
    '''Delete a label.'''
    model: Type[Label] = Label
    context_object_name: str = 'label'
    extra_context: Dict = CONTEXT_DELETE
    success_url: Union[str, Callable[..., Any]] = REVERSE_LABELS
    success_message: str = MSG_DELETED
    protected_data_url: Union[str, Callable[..., Any]] = REVERSE_LABELS
    protected_data_message: str = LABEL_USED_IN_TASK
