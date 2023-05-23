from django.urls import path, URLPattern
from typing import List

from .views import TasksListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskDetailView

urlpatterns: List[URLPattern] = [
    path('', TasksListView.as_view(), name='tasks'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete')
]
