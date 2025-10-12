from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = self.slug.lower()
        else:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    thumbnail = models.URLField()
    post_name = models.CharField(max_length=200, unique=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    # image = models.ImageField(upload_to='blog_images/')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.post_name:
            self.post_name = f"post-{self.id}"
        super(BlogPost, self).save(*args, **kwargs)
