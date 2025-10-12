from django.core.exceptions import ValidationError
from django.db import models

from .tagging import normalize_and_validate_tags

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    thumbnail = models.URLField()
    post_name = models.CharField(max_length=200, unique=True)
    tags = models.JSONField(default=list, blank=True)
    # image = models.ImageField(upload_to='blog_images/')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        normalised_tags, invalid_tags = normalize_and_validate_tags(self.tags)
        if invalid_tags:
            raise ValidationError({
                "tags": f"Invalid tag(s): {', '.join(sorted(set(invalid_tags)))}"
            })
        self.tags = normalised_tags
        if not self.post_name:
            self.post_name = f"post-{self.id}"
        super(BlogPost, self).save(*args, **kwargs)
