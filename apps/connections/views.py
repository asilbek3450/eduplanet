from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import UserCourse
from courses.models import Course


# Create your views here.

@login_required(login_url='login')
def enroll_course(request, course_id):
    # Get the course
    course = Course.objects.get(id=course_id)

    # Check if the user is already enrolled
    if UserCourse.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, "You are already enrolled in this course.")
    else:
        # Enroll the user in the course
        UserCourse.objects.create(user=request.user, course=course)
        messages.success(request, "You have successfully enrolled in the course.")

    return redirect('course_detail', course.slug)
