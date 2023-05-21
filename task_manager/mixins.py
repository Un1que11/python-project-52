from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.db.models import ProtectedError
from typing import Any, Union, Callable

from .constants import MSG_NO_PERMISSION, REVERSE_LOGIN, REVERSE_HOME


class AuthorizationPermissionMixin(LoginRequiredMixin):
    '''Sets access rules for unauthorized users.'''

    def handle_no_permission(self) -> HttpResponseRedirect:
        '''Sets rules when a page is unavailable to an unauthorized user.'''
        messages.warning(self.request, MSG_NO_PERMISSION)
        return redirect(REVERSE_LOGIN)


class ModifyPermissionMixin(LoginRequiredMixin):
    '''Sets access rules for an unauthenticated user.'''

    unpermission_message: str = 'Access denied message'
    unpermission_url: Union[str, Callable[..., Any]] = REVERSE_LOGIN

    def dispatch(self, request: HttpRequest,
                 *args: Any, **kwargs: Any) -> HttpResponse:
        '''Specifies access settings for the current user.
        Provides access if the user is authenticated.'''
        if request.user.id != self.get_object().id:
            messages.error(self.request, self.unpermission_message)
            return redirect(self.unpermission_url)
        return super().dispatch(request, *args, **kwargs)


class DeletionProtectionMixin:
    '''Sets the rules for handling the case of the impossibility of deleting data
    due to the protection of related data.'''

    protected_data_message: str = 'Entity deletion forbidden message'
    protected_data_url: Union[str, Callable[..., Any]] = REVERSE_HOME

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        '''Sends data to the server with protection check.'''
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, self.protected_data_message)
            return redirect(self.protected_data_url)
