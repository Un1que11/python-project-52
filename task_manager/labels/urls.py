from django.urls import path, URLPattern
from typing import List

from .views import LabelsListView, LabelCreateView, LabelUpdateView, LabelDeleteView
from .constants import LIST_LABELS, CREATE_LABEL, UPDATE_LABEL, DELETE_LABEL


urlpatterns: List[URLPattern] = [
    path('', LabelsListView.as_view(), name=LIST_LABELS),
    path('create/', LabelCreateView.as_view(), name=CREATE_LABEL),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name=UPDATE_LABEL),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name=DELETE_LABEL)
]
