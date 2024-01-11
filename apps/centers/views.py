from django.shortcuts import render, get_object_or_404
from centers.models import LearningCenter, Category
from courses.models import Course


# Create your views here.
def centers_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    learning_centers = LearningCenter.objects.filter(categories=category.id)
    context = {
        'category': category,
        'learning_centers': learning_centers,
    }
    return render(request, 'centers/centers_by_category.html', context)


def center_detail(request, slug):
    learning_center = get_object_or_404(LearningCenter, slug=slug)
    courses = Course.objects.filter(learning_center=learning_center)
    context = {
        'learning_center': learning_center,
        'courses': courses,
    }
    return render(request, 'centers/center_detail.html', context)
