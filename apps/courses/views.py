from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.db.models import Q
from centers.models import Category

from connections.models import UserCourse
from courses.models import Course
from site_content import get_course_detail_context
from users.views import account_context


def catalog(request):
    courses = Course.objects.select_related('instructor__user', 'category', 'learning_center')
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    if query:
        courses = courses.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category:
        courses = courses.filter(category__slug=category)
    return render(request, 'courses/catalog.html', {
        **account_context(request, 'Kurslar | EduPlanet', 'Barcha kurslar'),
        'page': Paginator(courses, 12).get_page(request.GET.get('page')),
        'categories': Category.objects.order_by('name'), 'query': query, 'selected_category': category,
    })


# Create your views here.
def course_detail(request, slug):
    course = get_object_or_404(Course.objects.select_related('learning_center', 'instructor__user', 'category'), slug=slug)
    is_user_enrolled = False
    if request.user.is_authenticated:
        is_user_enrolled = UserCourse.objects.filter(user=request.user, course=course).exists()

    context = get_course_detail_context(request, course, is_user_enrolled)
    return render(request, 'centers/course_detail.html', context)
