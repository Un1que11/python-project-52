from django.urls import path, URLPattern
from typing import List

from .views import StatusesListView, StatusCreateView, StatusUpdateView, StatusDeleteView
from .constants import LIST_STATUSES, CREATE_STATUS, UPDATE_STATUS, DELETE_STATUS


urlpatterns: List[URLPattern] = [
    path('', StatusesListView.as_view(), name=LIST_STATUSES),
    path('create/', StatusCreateView.as_view(), name=CREATE_STATUS),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name=UPDATE_STATUS),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name=DELETE_STATUS),
]
