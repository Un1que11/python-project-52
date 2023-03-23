from task_manager import views

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('', include('task_manager.users.urls')),
    path('admin/', admin.site.urls),
]
