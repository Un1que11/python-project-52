from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import User
from .forms import NewUserCreationForm


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/show.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserCreateView(CreateView):
    form_class = NewUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


class UserUpdateView(UpdateView):
    model = User


class UserDeleteView(DeleteView):
    model = User


class LoginUserView(LoginView):
    template_name = 'users/login.html'


class LogoutUsersView(LogoutView):
    pass
