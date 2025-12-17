from django.shortcuts import render, get_object_or_404
from .models import BlogPost


def blog_home(request):
    posts = list(BlogPost.objects.all().order_by('-date_posted'))
    all_tags = sorted({tag for post in posts for tag in post.tags})
    return render(
        request,
        'blog/blog_layout.html',
        {
            'posts': posts,
            'all_tags': all_tags,
        },
    )

def blog_detail(request, post_name):
    # Fetch the blog post by name or return a 404 if not found
    post = get_object_or_404(BlogPost, post_name=post_name)
    return render(request, 'blog/blog_detail.html', {'post': post, 'content': post.content})
