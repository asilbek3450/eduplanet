import re

from django.shortcuts import render, get_object_or_404

from courses.models import Course, VideoContent
from connections.models import UserCourse


# Create your views here.
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    video_contents = VideoContent.objects.filter(course=course)
    first_video = get_object_or_404(VideoContent, course=course, pk=1)

    # check user has enrolled this course
    user_course = UserCourse.objects.filter(user=request.user, course=course)
    is_user_enrolled = False
    if user_course.exists():
        is_user_enrolled = True

    context = {
        'course': course,
        'video_contents': video_contents,
        'first_video': first_video,
        'is_user_enrolled': is_user_enrolled
    }
    return render(request, 'centers/course_detail.html', context)
