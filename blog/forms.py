from django import forms
from .models import BlogPost
from tinymce.widgets import TinyMCE

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))

    class Meta:
        model = BlogPost
        fields = ['title', 'description', 'content', 'image'] # other fields if there are any