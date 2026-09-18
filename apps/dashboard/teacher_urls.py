from django.urls import path
from . import teacher_views as views

app_name = 'teacher'
urlpatterns = [
    path('', views.home, name='home'),
    path('courses/new/', views.course_form, name='course_create'),
    path('courses/<int:pk>/', views.course_form, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('courses/<int:course_pk>/lessons/new/', views.lesson_form, name='lesson_create'),
    path('lessons/<int:pk>/', views.lesson_form, name='lesson_edit'),
    path('lessons/<int:pk>/delete/', views.lesson_delete, name='lesson_delete'),
]
