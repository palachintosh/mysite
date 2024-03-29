"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from .views import based_blog
from blog.views import e_handler404, e_handler500
from django.conf.urls import handler404, handler500


urlpatterns = [
    path('', based_blog),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('blog_pl/', include('blog_pl.urls')),
    path('likes_and_statistics/', include('likes_and_statistics.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('bikes_monitoring/', include('bikes_monitoring.urls')),
    path('notes', include('notes.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('warehouse/', include('warehouse.urls'))
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = e_handler404
handler500 = e_handler500

#grunwald
