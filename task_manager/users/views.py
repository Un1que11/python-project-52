from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseForm
from typing import Dict, Type

from .models import User
from .forms import UserRegistrationForm, UserEditingForm
from ..mixins import ModifyPermissionMixin, DeletionProtectionMixin


class UsersListView(ListView):
    '''Show the list of users.'''
    model: Type[User] = User
    context_object_name: str = 'users'
    extra_context: Dict = {
        'page_title': _('Users'),
        'page_description': _('List of Task Manager Users.'),
        'page_h1': _('Users')
    }


class UserCreateView(SuccessMessageMixin, CreateView):
    '''Create a user.'''
    model: Type[User] = User
    extra_context: Dict = {
        'page_title': _('Registration'),
        'page_description': _('User Registration on Task Manager.'),
        'page_h1': _('Registration'),
        'button_text': _('Register')
    }
    form_class: Type[BaseForm] = UserRegistrationForm
    success_url = reverse_lazy('login')
    success_message: str = _('User successfully registered')


class UserUpdateView(ModifyPermissionMixin, LoginRequiredMixin,
                     SuccessMessageMixin, UpdateView):
    '''Change a user.'''
    model: Type[User] = User
    extra_context: Dict = {
        'page_title': _('User editing'),
        'page_description': _('User editing on Task Manager.'),
        'page_h1': _('User change'),
        'button_text': _('Change')
    }
    form_class: Type[BaseForm] = UserEditingForm
    success_url = reverse_lazy('users')
    success_message: str = _('User successfully updated')
    unpermission_url = reverse_lazy('users')
    unpermission_message: str = _('You do not have permission to modify another user')


class UserDeleteView(ModifyPermissionMixin, LoginRequiredMixin,
                     DeletionProtectionMixin, SuccessMessageMixin, DeleteView):
    '''Delete a user.'''
    model: Type[User] = User
    context_object_name: str = 'user'
    extra_context: Dict = {
        'page_title': _('User deleting'),
        'page_description': _('User deleting on Task Manager.'),
        'page_h1': _('Deleting a user'),
        'button_text': _('Yes, delete')
    }
    success_url = reverse_lazy('users')
    success_message: str = _('User successfully deleted')
    unpermission_url = reverse_lazy('users')
    unpermission_message: str = _('You do not have permission to modify another user')
    protected_data_url = reverse_lazy('users')
    protected_data_message: str = _('Cannot delete user because it is in use')
