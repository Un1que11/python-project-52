from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .constants import HOME, MSG_LOGIN, MSG_LOGOUT, TEMPLATE_INDEX


class HomePageView(TemplateView):
    '''Main page.'''
    template_name: str = TEMPLATE_INDEX


class UserLoginView(SuccessMessageMixin, LoginView):
    '''Log in into Task Manager.'''
    next_page: str = HOME
    success_message: str = MSG_LOGIN


class UserLogoutView(LogoutView):
    '''Log out from Task Manager.'''
    next_page: str = HOME

    def get(self, request, *args, **kwargs):
        messages.success(self.request, MSG_LOGOUT)
        return super().get(request, *args, **kwargs)
