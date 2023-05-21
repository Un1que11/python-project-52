from django.urls import path, URLPattern
from typing import List

from .views import TasksListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskDetailView
from .constants import LIST_TASKS, CREATE_TASK, UPDATE_TASK, DELETE_TASK, DETAIL_TASK


urlpatterns: List[URLPattern] = [
    path('', TasksListView.as_view(), name=LIST_TASKS),
    path('create/', TaskCreateView.as_view(), name=CREATE_TASK),
    path('<int:pk>/', TaskDetailView.as_view(), name=DETAIL_TASK),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name=UPDATE_TASK),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name=DELETE_TASK)
]
