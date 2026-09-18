from django.urls import path

from courses.views import course_detail, catalog

urlpatterns = [
    path('', catalog, name='course_catalog'),
    path('<str:slug>/', course_detail, name="course_detail"),

]

