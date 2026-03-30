from django.shortcuts import get_object_or_404, render

from connections.models import UserCourse
from courses.models import Course
from site_content import get_course_detail_context


# Create your views here.
def course_detail(request, slug):
    course = get_object_or_404(Course.objects.select_related('learning_center'), slug=slug)
    is_user_enrolled = False
    if request.user.is_authenticated:
        is_user_enrolled = UserCourse.objects.filter(user=request.user, course=course).exists()

    context = get_course_detail_context(request, course, is_user_enrolled)
    return render(request, 'centers/course_detail.html', context)
