from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from connections.models import UserCourse
from site_content import build_common_context, get_contact_success_context, get_language, global_keywords, with_lang
from .forms import UserSigninForm, UserSignupForm, UserUpdateForm
from .models import User, InstructorProfile
from courses.models import Course
from django.core.paginator import Paginator


def localize_account_form(form, lang):
    labels = {
        "uz": {"username": "Foydalanuvchi nomi", "password": "Parol", "password1": "Parol", "password2": "Parolni tasdiqlang"},
        "en": {"username": "Username", "password": "Password", "password1": "Password", "password2": "Confirm password"},
        "ru": {"username": "Имя пользователя", "password": "Пароль", "password1": "Пароль", "password2": "Подтвердите пароль"},
    }
    for field_name, placeholder in labels[lang].items():
        if field_name in form.fields:
            form.fields[field_name].widget.attrs["placeholder"] = placeholder
    return form


def account_context(request, title, description):
    seo = {
        'title': title,
        'description': description,
        'keywords': global_keywords(['account', 'eduplanet']),
        'og_title': title,
        'og_description': description,
        'og_image': 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=1200&q=80',
        'structured_data': '{"@context": "https://schema.org", "@type": "WebPage", "name": "%s"}' % title,
    }
    return build_common_context(request, seo)


# user signup and save user to database
def user_signup(request):
    lang = get_language(request)
    error = ''
    if request.method == 'POST':
        form = localize_account_form(UserSignupForm(request.POST), lang)
        if form.is_valid():
            form.save()
            messages.success(request, "Akkauntingiz yaratildi. Endi tizimga kirishingiz mumkin.")
        error = "Ma'lumotlar to'g'ri kiritilmagan"
    else:
        form = localize_account_form(UserSignupForm(), lang)
    context = account_context(request, 'Ro\'yxatdan o\'tish | EduPlanet', 'EduPlanet platformasida akkaunt ochib kurslarga yoziling va personal learning dashboardga ega bo\'ling.')
    context.update({'form': form, 'error': error})
    return render(request, 'auth/register.html', context)


def user_login(request):
    lang = get_language(request)
    next_url = request.POST.get('next') or request.GET.get('next', '')
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        next_url = ''
    if request.method == 'POST':
        form = localize_account_form(UserSigninForm(request.POST), lang)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Xush kelibsiz!')
                return redirect(next_url or with_lang('/users/profile/', lang))
            messages.error(request, 'Username yoki parol noto\'g\'ri')
    else:
        form = localize_account_form(UserSigninForm(), lang)
    context = account_context(request, 'Kirish | EduPlanet', 'EduPlanet akkauntingizga kirib kurslar, saved content va learning dashboardga ulaning.')
    context.update({'form': form, 'next_url': next_url})
    return render(request, 'auth/login.html', context)


@login_required(login_url='login')
def user_logout(request):
    lang = get_language(request)
    logout(request)
    messages.success(request, 'Tizimdan chiqdingiz.')
    return redirect(with_lang('/', lang))


@login_required(login_url='login')
def profile_page(request):
    user_profile = request.user
    enrolled_courses = UserCourse.objects.select_related('course').filter(user=request.user.id)
    context = account_context(request, 'Profil | EduPlanet', 'EduPlanet learning profile, enrolled courses va personal progress overview.')
    teacher = InstructorProfile.objects.filter(user=request.user).first()
    teaching_courses = Course.objects.filter(instructor=teacher).select_related('category').prefetch_related('video_contents') if teacher else Course.objects.none()
    context.update({
        'teacher_profile': teacher,
        'teaching_page': Paginator(teaching_courses, 8).get_page(request.GET.get('page')),
        'user_profile': user_profile,
        'enrolled_courses': enrolled_courses,
    })
    return render(request, 'auth/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    user_profile = User.objects.get(id=request.user.id)
    lang = get_language(request)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil ma\'lumotlari yangilandi.')
            return redirect(with_lang('/users/profile/', lang))
    else:
        form = UserUpdateForm(instance=user_profile)
    context = account_context(request, 'Profilni tahrirlash | EduPlanet', 'EduPlanet profilingizdagi shaxsiy ma\'lumotlarni va learning experience sozlamalarini yangilang.')
    context.update({'form': form, 'user_profile': user_profile})
    return render(request, 'auth/edit_profile.html', context)


def contact_us_success(request):
    context = get_contact_success_context(request)
    return render(request, 'contact_us_success.html', context)


def page_not_found(request, exception):
    return render(request, '404.html', account_context(request, 'Sahifa topilmadi | EduPlanet', 'Sahifa topilmadi'), status=404)
