from django.db import models
from django.utils.translation import gettext_lazy


class Status(models.Model):
    name = models.CharField(
        verbose_name=gettext_lazy('name'),
        max_length=40, unique=True, blank=False
    )
    date_created = models.DateTimeField(
        verbose_name=gettext_lazy('created at'),
        auto_now_add=True
    )
    date_modified = models.DateTimeField(
        verbose_name=gettext_lazy('modified at'),
        auto_now=True
    )

    class Meta:
        verbose_name: str = gettext_lazy('status')
        verbose_name_plural: str = gettext_lazy('statuses')

    def __str__(self) -> str:
        return self.name
