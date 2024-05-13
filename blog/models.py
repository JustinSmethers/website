from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    thumbnail = models.URLField()
    post_name = models.CharField(max_length=200, unique=True)
    # image = models.ImageField(upload_to='blog_images/')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.post_name:
            self.post_name = f"post-{self.id}"
        super(BlogPost, self).save(*args, **kwargs)