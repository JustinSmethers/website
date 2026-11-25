from django.contrib import admin
from django.urls import include, path

from blog.views import blog_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog_home, name='home'),
    path('blog/', include('blog.urls', namespace='blog'))
]
