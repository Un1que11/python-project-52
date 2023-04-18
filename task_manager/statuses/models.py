from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
