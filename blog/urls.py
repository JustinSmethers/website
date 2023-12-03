from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_home, name='index'),
    path('post/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('create/', views.create_blog_post, name='create_blog_post'),
]
