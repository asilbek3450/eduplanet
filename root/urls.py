"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from django.conf import settings
from django.views.generic import RedirectView
from .media import public_media

urlpatterns = [
    path('django-admin/', admin.site.urls),
    # Accept the commonly typed URL without a trailing slash as well.
    path('admin/login', RedirectView.as_view(url='/admin/login/', permanent=False)),
    path('admin/', include('dashboard.urls')),
    path('', include("apps.urls")),
    # WhiteNoise serves static assets, but deliberately does not serve uploads.
    # This fallback is required when DEBUG=False and no proxy/CDN owns /media/.
    path('media/<path:path>', public_media, name='public-media'),
]
# Serving the media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

handler404 = 'users.views.page_not_found'
