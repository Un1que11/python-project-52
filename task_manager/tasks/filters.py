"""Filters for task list view."""

from django import forms
from django.utils.translation import gettext_lazy

from django_filters import FilterSet, BooleanFilter, ChoiceFilter

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TasksFilter(FilterSet):
    """Define filers for tasks list."""
    labels_query = Label.objects.values_list('id', 'name')
    labels = ChoiceFilter(label=gettext_lazy('Label'), choices=labels_query)
    self_tasks = BooleanFilter(
        label=gettext_lazy('Current user tasks'),
        widget=forms.CheckboxInput(),
        method='get_self_tasks',
    )

    class Meta:
        model = Task
        fields = ['status', 'executor']

    def get_self_tasks(self, queryset, name, value):
        """Filter current user tasks."""
        if value:
            queryset = queryset.filter(author=self.request.user)
        return queryset
