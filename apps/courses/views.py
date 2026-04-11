from django.shortcuts import get_object_or_404, render

from connections.models import UserCourse, UserCourseComment, UserCourseRating
from courses.models import Course
from site_content import get_course_detail_context


def course_detail(request, slug):
    course = get_object_or_404(Course.objects.select_related('learning_center'), slug=slug)
    is_user_enrolled = False
    user_rating = None

    if request.user.is_authenticated:
        is_user_enrolled = UserCourse.objects.filter(user=request.user, course=course).exists()
        rating_obj = UserCourseRating.objects.filter(user=request.user, course=course).first()
        user_rating = rating_obj.rating if rating_obj else None

    comments = (
        UserCourseComment.objects
        .select_related('user')
        .filter(course=course)
        .order_by('-created_at')
    )

    context = get_course_detail_context(request, course, is_user_enrolled)
    context.update({
        'comments': comments,
        'user_rating': user_rating,
    })
    return render(request, 'centers/course_detail.html', context)
