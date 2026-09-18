from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from users.views import account_context
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from courses.models import Course, VideoContent
from users.models import InstructorProfile
from .forms import CourseForm, VideoContentForm


def teacher_required(view):
    @login_required(login_url='login')
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        request.teacher = InstructorProfile.objects.filter(user=request.user, user__is_active=True).first()
        if request.teacher is None:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapped


@teacher_required
def home(request):
    return redirect('profile')


@teacher_required
def course_form(request, pk=None):
    course = get_object_or_404(Course, pk=pk, instructor=request.teacher) if pk else Course(instructor=request.teacher)
    form = CourseForm(request.POST if request.method == 'POST' else None, instance=course)
    for field in ('instructor', 'featured', 'hours_watched', 'lessons_count'):
        form.fields.pop(field, None)
    form.fields['category'].required = True
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'teacher/form.html', {**account_context(request, 'Profil | EduPlanet', 'Kurs va darslarni boshqarish'), 'form': style_form(form), 'title': 'Kurs ma’lumotlari'})


@teacher_required
def lesson_form(request, course_pk=None, pk=None):
    if pk:
        lesson = get_object_or_404(VideoContent, pk=pk, course__instructor=request.teacher)
    else:
        lesson = VideoContent(course=get_object_or_404(Course, pk=course_pk, instructor=request.teacher))
    form = VideoContentForm(request.POST if request.method == 'POST' else None, instance=lesson)
    form.fields.pop('course')
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'teacher/form.html', {**account_context(request, 'Profil | EduPlanet', 'Kurs va darslarni boshqarish'), 'form': style_form(form), 'title': 'Dars ma’lumotlari'})


@teacher_required
@require_POST
def course_delete(request, pk):
    get_object_or_404(Course, pk=pk, instructor=request.teacher).delete()
    return redirect('profile')


@teacher_required
@require_POST
def lesson_delete(request, pk):
    get_object_or_404(VideoContent, pk=pk, course__instructor=request.teacher).delete()
    return redirect('profile')


def style_form(form):
    for field in form.fields.values():
        field.widget.attrs['class'] = 'w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100'
    return form
