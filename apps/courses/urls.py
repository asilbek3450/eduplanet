from django.urls import path

from courses.views import course_detail

urlpatterns = [
    path('<str:slug>/', course_detail, name="course_detail"),

]

