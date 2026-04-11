from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from courses.models import Course
from site_content import get_language, with_lang
from .models import UserCourse, UserCourseComment, UserCourseRating


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


@login_required(login_url='login')
@require_POST
def add_comment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lang = get_language(request)
    text = request.POST.get('text', '').strip()

    if not UserCourse.objects.filter(user=request.user, course=course).exists():
        messages.error(request, "Izoh qoldirish uchun avval kursga yozilishingiz kerak.")
        return redirect(with_lang(f'/courses/{course.slug}/', lang))

    if not text:
        messages.error(request, "Izoh matni bo'sh bo'lishi mumkin emas.")
        return redirect(with_lang(f'/courses/{course.slug}/', lang))

    if len(text) > 1000:
        messages.error(request, "Izoh 1000 belgidan oshmasligi kerak.")
        return redirect(with_lang(f'/courses/{course.slug}/', lang))

    UserCourseComment.objects.create(user=request.user, course=course, text=text)
    messages.success(request, "Izohingiz qo'shildi.")
    return redirect(with_lang(f'/courses/{course.slug}/', lang) + '#comments')


@login_required(login_url='login')
@require_POST
def submit_rating(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lang = get_language(request)

    if not UserCourse.objects.filter(user=request.user, course=course).exists():
        messages.error(request, "Baholash uchun avval kursga yozilishingiz kerak.")
        return redirect(with_lang(f'/courses/{course.slug}/', lang))

    try:
        rating_value = int(request.POST.get('rating', 0))
    except (ValueError, TypeError):
        rating_value = 0

    if rating_value not in range(1, 6):
        messages.error(request, "Baho 1 dan 5 gacha bo'lishi kerak.")
        return redirect(with_lang(f'/courses/{course.slug}/', lang))

    UserCourseRating.objects.update_or_create(
        user=request.user,
        course=course,
        defaults={'rating': rating_value},
    )
    course.update_rating()
    messages.success(request, f"Bahoyingiz ({rating_value} ★) saqlandi.")
    return redirect(with_lang(f'/courses/{course.slug}/', lang) + '#comments')
