from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from typing import Dict, Any, Tuple, Union, Callable, Type

from .models import Status
from .constants import REVERSE_STATUSES, NAME, \
    CONTEXT_LIST, CONTEXT_CREATE, CONTEXT_UPDATE, CONTEXT_DELETE, \
    MSG_CREATED, MSG_UPDATED, MSG_DELETED, STATUS_USED_IN_TASK
from ..mixins import AuthorizationPermissionMixin, DeletionProtectionMixin


class StatusesListView(AuthorizationPermissionMixin, ListView):
    '''Show the list of statuses.'''
    model: Type[Status] = Status
    context_object_name: str = 'statuses'
    extra_context: Dict = CONTEXT_LIST


class StatusCreateView(AuthorizationPermissionMixin,
                       SuccessMessageMixin, CreateView):
    '''Create a status.'''
    model: Type[Status] = Status
    extra_context: Dict = CONTEXT_CREATE
    fields: Tuple = (NAME,)
    success_url: Union[str, Callable[..., Any]] = REVERSE_STATUSES
    success_message: str = MSG_CREATED


class StatusUpdateView(AuthorizationPermissionMixin,
                       SuccessMessageMixin, UpdateView):
    '''Change a status.'''
    model: Type[Status] = Status
    extra_context: Dict = CONTEXT_UPDATE
    fields: Tuple = (NAME,)
    success_url: Union[str, Callable[..., Any]] = REVERSE_STATUSES
    success_message: str = MSG_UPDATED


class StatusDeleteView(AuthorizationPermissionMixin,
                       DeletionProtectionMixin, SuccessMessageMixin, DeleteView):
    '''Delete a status.'''
    model: Type[Status] = Status
    extra_context: Dict = CONTEXT_DELETE
    context_object_name: str = 'status'
    success_url: Union[str, Callable[..., Any]] = REVERSE_STATUSES
    success_message: str = MSG_DELETED
    protected_data_url: Union[str, Callable[..., Any]] = REVERSE_STATUSES
    protected_data_message: str = STATUS_USED_IN_TASK
