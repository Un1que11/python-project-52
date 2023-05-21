from django.db import models
from django.utils.translation import gettext_lazy

from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(
        verbose_name=gettext_lazy('name'),
        max_length=50, blank=False,
        help_text=gettext_lazy(
            "Required. 50 characters or fewer."
        ),
        error_messages={
            "blank": gettext_lazy(
                "The task name is required."
            ),
        }
    )
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT,
        verbose_name=gettext_lazy('status')
    )
    description = models.TextField(
        verbose_name=gettext_lazy('description'),
        max_length=5000
    )
    author = models.ForeignKey(
        User, on_delete=models.PROTECT,
        verbose_name=gettext_lazy('author'), related_name="author_id"
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT,
        verbose_name=gettext_lazy('executor'), related_name="executor_id",
        blank=True, null=True
    )
    date_created = models.DateTimeField(
        verbose_name=gettext_lazy('created at'),
        auto_now_add=True
    )
    date_modified = models.DateTimeField(
        verbose_name=gettext_lazy('modified at'),
        auto_now=True
    )
    labels = models.ManyToManyField(
        Label,
        verbose_name=gettext_lazy('labels'),
        through='TaskLabel', through_fields=('task', 'label'),
        blank=True, help_text=gettext_lazy(
            "You can select multiple labels."
        )
    )

    class Meta:
        verbose_name: str = gettext_lazy('task')
        verbose_name_plural: str = gettext_lazy('tasks')

    def __str__(self) -> str:
        return self.name


class TaskLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
