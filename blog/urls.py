from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_home, name='index'),
    path('post/<str:post_name>/', views.blog_detail, name='blog_detail'),
]
