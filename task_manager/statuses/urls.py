from task_manager.statuses import views

from django.urls import path

urlpatterns = [
    path('', views.StatusListView.as_view(), name='statuses'),
    path('create/', views.StatusCreateView.as_view(), name='status-create'),
    path('<int:pk>/update/', views.StatusUpdateView.as_view(), name='status-update'),
    path('<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status-delete'),
]
