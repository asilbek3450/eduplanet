from django.shortcuts import render
from .models import LearningCenter, Courses


# Create your views here.
def dashboard(request):
    learning_centers = LearningCenter.objects.all()
    context = {
        'learning_centers': learning_centers
    }
    return render(request, 'index.html', context)


def programming(request):
    centers = LearningCenter.objects.all()
    context = {
        'centers': centers
    }
    return render(request, 'centers/programming.html', context)


def programming_detail(request, pk):
    centers = LearningCenter.objects.all()
    course = Courses.objects.get(pk=pk)
    context = {
        'centers': centers,
        'course': course
    }
    return render(request, 'centers/programming_detail.html', context)
