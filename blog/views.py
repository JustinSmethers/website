from django.shortcuts import render, get_object_or_404
from .models import BlogPost


def blog_home(request):
    # ... Any logic for fetching blog posts, etc.
    posts = BlogPost.objects.all().order_by('-date_posted')
    return render(request, 'blog/blog_layout.html', {'posts': posts})

def blog_detail(request, post_id):
    # Fetch the blog post by ID or return a 404 if not found
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'blog/blog_detail.html', {'post': post, 'content': post.content})
