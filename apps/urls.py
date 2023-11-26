from django.urls import path, include

from .views import dashboard, programming, programming_detail

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('programming/', programming, name="programming"),
    path('programming/<int:pk>/', programming_detail, name="programming_detail"),
]
