from django.db import models

# Create your models here.
class Post(models.Model):
    """A model representing a blog post"""
    title = models.CharField(max_length=255)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, primary_key=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-pub_date"]
