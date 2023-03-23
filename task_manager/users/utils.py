from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _


class UserPermissionsMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().id:
            messages.add_message(
                    request,
                    messages.ERROR,
                    _('You have no rights to change another user.')
                    )
            return redirect(reverse_lazy('users-list'))

        return super().dispatch(request, *args, **kwargs)


class LoginRequiredMessageMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                    request,
                    messages.ERROR,
                    _('You are not authorized! Please, log in.'))
            return redirect(reverse_lazy('login'))

        return super().dispatch(request, *args, **kwargs)
