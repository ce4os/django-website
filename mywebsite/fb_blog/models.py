from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    """A model representing a blog post"""
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-created_at"]
