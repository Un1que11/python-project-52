from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class HomePageView(TemplateView):
    '''Main page.'''
    template_name: str = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    '''Log in into Task Manager.'''
    next_page: str = 'home'
    success_message: str = _('You are logged in')


class UserLogoutView(LogoutView):
    '''Log out from Task Manager.'''
    next_page: str = 'home'

    def get(self, request, *args, **kwargs):
        messages.success(self.request, _('You are logged out'))
        return super().get(request, *args, **kwargs)
