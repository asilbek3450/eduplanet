import re

from django.shortcuts import render, get_object_or_404

from courses.models import Course, VideoContent


# Create your views here.
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    video_contents = VideoContent.objects.filter(course=course)
    first_video = get_object_or_404(VideoContent, course=course, pk=1)
    context = {
        'course': course,
        'video_contents': video_contents,
        'first_video': first_video,
    }
    return render(request, 'centers/course_detail.html', context)
