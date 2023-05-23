from django.urls import path, URLPattern
from typing import List

from .views import LabelsListView, LabelCreateView, LabelUpdateView, LabelDeleteView

urlpatterns: List[URLPattern] = [
    path('', LabelsListView.as_view(), name='labels'),
    path('create/', LabelCreateView.as_view(), name='label_create'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='label_update'),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='label_delete')
]
