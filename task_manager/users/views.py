from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import User


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/users.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User


class UserUpdateView(UpdateView):
    model = User


class UserDeleteView(DeleteView):
    model = User
