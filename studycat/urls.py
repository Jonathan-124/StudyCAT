"""studycat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
# Imports for serving media images during development...
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/', include('api.urls')),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('profiles/', include(('userprofiles.urls', 'userprofiles'), namespace='userprofiles')),
    path('lessons/', include(('lessons.urls', 'lessons'), namespace='lessons')),
    path('units/', include(('units.urls', 'units'), namespace='units')),
    path('curricula/', include('curricula.urls')),
    path('placement/', include(('placement.urls', 'placement'), namespace='placement')),
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # serving images during development
