from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'blog'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='home', permanent=True, query_string=True), name='index'),
    path('post/<str:post_name>/', views.blog_detail, name='blog_detail'),
]
