from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from courses.models import Course
from site_content import get_language, with_lang
from .models import UserCourse


# Create your views here.
@login_required(login_url='login')
@require_POST
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lang = get_language(request)

    with transaction.atomic():
        _, created = UserCourse.objects.get_or_create(user=request.user, course=course)

    if not created:
        messages.warning(request, "Siz ushbu kursga allaqachon yozilgansiz.")
    else:
        messages.success(request, "Kursga muvaffaqiyatli yozildingiz.")

    return redirect(with_lang(f'/courses/{course.slug}/', lang))
