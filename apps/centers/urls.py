from django.urls import path

from .views import centers_by_category, center_detail

urlpatterns = [
    path('category/<str:slug>/', centers_by_category, name="centers_by_category"),
    path('<str:slug>/', center_detail, name="center_detail"),
]

