from task_manager import views

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.hello),
    path('admin/', admin.site.urls),
]
