from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required
import markdown


def blog_home(request):
    # ... Any logic for fetching blog posts, etc.
    posts = BlogPost.objects.all().order_by('-date_posted')
    return render(request, 'blog/blog_layout.html', {'posts': posts})

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    post_content = markdown.markdown(post.content)
    return render(request, 'blog/blog_detail.html', {'post': post, 'content': post_content})
