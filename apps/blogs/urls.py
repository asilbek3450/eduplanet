from django.urls import path

from .views import dashboard, blog_list, blog_detail

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('blogs/', blog_list, name='blog_list'),
    path('blogs/<slug:slug>/', blog_detail, name='blog_detail'),
]
