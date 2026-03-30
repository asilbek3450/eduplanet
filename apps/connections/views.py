from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from courses.models import Course
from site_content import get_language, with_lang
from .models import UserCourse


# Create your views here.
@login_required(login_url='login')
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lang = get_language(request)

    if UserCourse.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, "Siz ushbu kursga allaqachon yozilgansiz.")
    else:
        UserCourse.objects.create(user=request.user, course=course)
        messages.success(request, "Kursga muvaffaqiyatli yozildingiz.")

    return redirect(with_lang(f'/courses/{course.slug}/', lang))
