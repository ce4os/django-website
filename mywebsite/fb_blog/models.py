from datetime import datetime

from django.db import models
from django.utils import timezone


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    update = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]

    