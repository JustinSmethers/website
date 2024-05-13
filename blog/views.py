from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import markdown


def blog_home(request):
    # ... Any logic for fetching blog posts, etc.
    posts = BlogPost.objects.all().order_by('-date_posted')
    return render(request, 'blog/blog_layout.html', {'posts': posts})

def blog_detail(request, post_id):
    # Fetch the blog post by ID or return a 404 if not found
    post = get_object_or_404(BlogPost, id=post_id)

    extensions = [
        "markdown.extensions.fenced_code",      # Allows code blocks to be fenced by ``` or ~~~
        "markdown.extensions.tables",           # Allows tables to be created using | and -
        "markdown.extensions.toc",              # Allows a table of contents to be generated
        "markdown.extensions.codehilite",       # Allows syntax highlighting
        "markdown.extensions.extra"             # Adds several miscellaneous extensions
    # ])
    ]

    extension_configs = {
        "codehilite": {
            'use_pygments': True,
            'css_class': 'highlight',
            'guess_lang': False
        },
    }

    md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)

    # Convert Markdown text to HTML
    post_content = mark_safe(md.convert(post.content))

    print(post_content)

    # post_content = markdown.markdown(post.content)
    return render(request, 'blog/blog_detail.html', {'post': post, 'content': post_content})





# from django.shortcuts import render, get_object_or_404, redirect
# from .models import BlogPost
# from django.contrib.auth.decorators import login_required
# import markdown
# # from markdown.extensions.toc import TocExtension
# # from pymdownx.superfences import SuperFencesCodeExtension
# # from pymdownx.extra import ExtraExtension
# # from pymdownx.magiclink import MagiclinkExtension
# # from pymdownx.tabbed import TabbedExtension


# def blog_home(request):
#     # ... Any logic for fetching blog posts, etc.
#     posts = BlogPost.objects.all().order_by('-date_posted')
#     return render(request, 'blog/blog_layout.html', {'posts': posts})

# def blog_detail(request, post_id):
#     post = get_object_or_404(BlogPost, id=post_id)

#     # Setup Markdown with pymdown-extensions
#     # md = markdown.Markdown(extensions=[
#     extensions = [
#         'extra',                 # Adds several miscellaneous extensions
#         'toc'                    # Table of contents
#     ]
#     # ])

#     # Convert Markdown text to HTML
#     # post_content = md.convert(post.content)
#     # post_content = markdown.markdown(post.content, extensions=extensions)

#     with open(post.content, 'r') as f:
#         text = f.read()
#         post_content = markdown.markdown(text, extensions=extensions)


#     return render(request, 'blog/blog_detail.html', {'post': post, 'content': post_content})
