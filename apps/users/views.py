from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from connections.models import UserCourse
from site_content import build_common_context, ensure_platform_content, get_contact_success_context, get_language, global_keywords, with_lang
from .forms import UserSigninForm, UserSignupForm, UserUpdateForm


def account_context(request, title, description):
    ensure_platform_content()
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


def user_signup(request):
    lang = get_language(request)
    error = ''
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Akkauntingiz yaratildi. Endi tizimga kirishingiz mumkin.")
            return redirect(with_lang('/users/login/', lang))
        error = "Ma'lumotlar to'g'ri kiritilmagan"
    else:
        form = UserSignupForm()
    context = account_context(request, 'Ro\'yxatdan o\'tish | EduPlanet', 'EduPlanet platformasida akkaunt ochib kurslarga yoziling va personal learning dashboardga ega bo\'ling.')
    context.update({'form': form, 'error': error})
    return render(request, 'auth/register.html', context)


def user_login(request):
    lang = get_language(request)
    if request.user.is_authenticated:
        return redirect(with_lang('/users/profile/', lang))
    if request.method == 'POST':
        form = UserSigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Xush kelibsiz!')
                next_url = request.GET.get('next', with_lang('/', lang))
                return redirect(next_url)
            messages.error(request, 'Username yoki parol noto\'g\'ri')
    else:
        form = UserSigninForm()
    context = account_context(request, 'Kirish | EduPlanet', 'EduPlanet akkauntingizga kirib kurslar, saved content va learning dashboardga ulaning.')
    context.update({'form': form})
    return render(request, 'auth/login.html', context)


@login_required(login_url='login')
def user_logout(request):
    lang = get_language(request)
    logout(request)
    messages.success(request, 'Tizimdan chiqdingiz.')
    return redirect(with_lang('/', lang))


@login_required(login_url='login')
def profile_page(request):
    enrolled_courses = (
        UserCourse.objects
        .select_related('course', 'course__learning_center')
        .filter(user=request.user)
        .order_by('-enrolled_date')
    )
    context = account_context(request, 'Profil | EduPlanet', 'EduPlanet learning profile, enrolled courses va personal progress overview.')
    context.update({
        'user_profile': request.user,
        'enrolled_courses': enrolled_courses,
    })
    return render(request, 'auth/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    lang = get_language(request)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil ma\'lumotlari yangilandi.')
            return redirect(with_lang('/users/profile/', lang))
    else:
        form = UserUpdateForm(instance=request.user)
    context = account_context(request, 'Profilni tahrirlash | EduPlanet', 'EduPlanet profilingizdagi shaxsiy ma\'lumotlarni va learning experience sozlamalarini yangilang.')
    context.update({'form': form, 'user_profile': request.user})
    return render(request, 'auth/edit_profile.html', context)


def contact_us_success(request):
    context = get_contact_success_context(request)
    return render(request, 'contact_us_success.html', context)
