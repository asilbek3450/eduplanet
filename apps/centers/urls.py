from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import centers_by_category, center_detail

urlpatterns = [
    path('category/<str:slug>/', centers_by_category, name="centers_by_category"),
    path('<str:slug>/', center_detail, name="center_detail"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
