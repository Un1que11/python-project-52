from task_manager import views

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.Index.as_view()),
    path('admin/', admin.site.urls),
]
