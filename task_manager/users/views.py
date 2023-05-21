from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseForm
from typing import Dict, Any, Union, Callable, Type

from .models import User
from .forms import UserRegistrationForm, UserEditingForm
from .constants import REVERSE_USERS, REVERSE_LOGIN, \
    CONTEXT_LIST, CONTEXT_CREATE, CONTEXT_UPDATE, CONTEXT_DELETE, \
    MSG_REGISTERED, MSG_UPDATED, MSG_DELETED, MSG_UNPERMISSION_TO_MODIFY, \
    USER_USED_IN_TASK
from ..mixins import ModifyPermissionMixin, DeletionProtectionMixin


class UsersListView(ListView):
    '''Show the list of users.'''
    model: Type[User] = User
    context_object_name: str = 'users'
    extra_context: Dict = CONTEXT_LIST


class UserCreateView(SuccessMessageMixin, CreateView):
    '''Create a user.'''
    model: Type[User] = User
    extra_context: Dict = CONTEXT_CREATE
    form_class: Type[BaseForm] = UserRegistrationForm
    success_url: Union[str, Callable[..., Any]] = REVERSE_LOGIN
    success_message: str = MSG_REGISTERED


class UserUpdateView(ModifyPermissionMixin, LoginRequiredMixin,
                     SuccessMessageMixin, UpdateView):
    '''Change a user.'''
    model: Type[User] = User
    extra_context: Dict = CONTEXT_UPDATE
    form_class: Type[BaseForm] = UserEditingForm
    success_url: Union[str, Callable[..., Any]] = REVERSE_USERS
    success_message: str = MSG_UPDATED
    unpermission_url: Union[str, Callable[..., Any]] = REVERSE_USERS
    unpermission_message: str = MSG_UNPERMISSION_TO_MODIFY


class UserDeleteView(ModifyPermissionMixin, LoginRequiredMixin,
                     DeletionProtectionMixin, SuccessMessageMixin, DeleteView):
    '''Delete a user.'''
    model: Type[User] = User
    context_object_name: str = 'user'
    extra_context: Dict = CONTEXT_DELETE
    success_url: Union[str, Callable[..., Any]] = REVERSE_USERS
    success_message: str = MSG_DELETED
    unpermission_url: Union[str, Callable[..., Any]] = REVERSE_USERS
    unpermission_message: str = MSG_UNPERMISSION_TO_MODIFY
    protected_data_url: Union[str, Callable[..., Any]] = REVERSE_USERS
    protected_data_message: str = USER_USED_IN_TASK
