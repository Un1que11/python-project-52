from django.urls import path, URLPattern
from typing import List

from .views import UsersListView, UserCreateView, UserUpdateView, UserDeleteView
from .constants import LIST_USERS, CREATE_USER, UPDATE_USER, DELETE_USER


urlpatterns: List[URLPattern] = [
    path('', UsersListView.as_view(), name=LIST_USERS),
    path('create/', UserCreateView.as_view(), name=CREATE_USER),
    path('<int:pk>/update/', UserUpdateView.as_view(), name=UPDATE_USER),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name=DELETE_USER)
]
