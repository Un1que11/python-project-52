from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from .utils import UserPermissionsMixin, LoginRequiredMessageMixin
from .forms import NewUserCreationForm


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/show.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = NewUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully sign up')


class UserUpdateView(
        SuccessMessageMixin,
        LoginRequiredMessageMixin,
        UserPermissionsMixin,
        LoginRequiredMixin,
        UpdateView
        ):
    model = get_user_model()
    form_class = NewUserCreationForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users-list')
    success_message = _('User successfully changed')


class UserDeleteView(
        SuccessMessageMixin,
        LoginRequiredMessageMixin,
        UserPermissionsMixin,
        LoginRequiredMixin,
        DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users-list')
    success_message = _('User successfully deleted')


class LoginUserView(SuccessMessageMixin, LoginView):
    model = get_user_model()
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_message = _('You are logged in')


class LogoutUsersView(SuccessMessageMixin, LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, _('You are unlogged'))
        return super().dispatch(request, *args, **kwargs)
