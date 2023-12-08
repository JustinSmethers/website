from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    thumbnail = models.URLField()
    # image = models.ImageField(upload_to='blog_images/')
