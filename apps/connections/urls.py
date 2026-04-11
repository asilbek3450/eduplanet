from django.urls import path

from .views import enroll_course, add_comment, submit_rating

urlpatterns = [
    path('enrol_course/<int:course_id>/', enroll_course, name='enroll_course'),
    path('comment/<int:course_id>/', add_comment, name='add_comment'),
    path('rating/<int:course_id>/', submit_rating, name='submit_rating'),
]
