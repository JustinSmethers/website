from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "post_name", "display_tags")
    search_fields = ("title", "description", "post_name", "tags")

    @staticmethod
    def display_tags(obj):
        return ", ".join(obj.tags or [])

    display_tags.short_description = "Tags"
