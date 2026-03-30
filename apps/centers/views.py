from django.shortcuts import get_object_or_404, render

from centers.models import Category, LearningCenter
from site_content import get_center_detail_context, get_centers_by_category_context


# Create your views here.
def centers_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context = get_centers_by_category_context(request, category)
    return render(request, 'centers/centers_by_category.html', context)


def center_detail(request, slug):
    learning_center = get_object_or_404(LearningCenter.objects.prefetch_related('categories', 'courses'), slug=slug)
    context = get_center_detail_context(request, learning_center)
    return render(request, 'centers/center_detail.html', context)
