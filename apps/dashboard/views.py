from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from blogs.models import BlogImage, BlogPost
from centers.models import Category, LearningCenter
from connections.models import (
    Testimonial,
    UserCourse,
    UserCourseComment,
    UserCourseRating,
)
from courses.models import Course, VideoContent
from users.models import ContactUs, InstructorProfile, User

from .forms import (
    AdminLoginForm,
    BlogImageForm,
    BlogPostForm,
    CategoryForm,
    ContactUsResponseForm,
    CourseForm,
    InstructorProfileForm,
    LearningCenterForm,
    TestimonialForm,
    UserAdminForm,
    VideoContentForm,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def staff_required(view):
    return login_required(login_url='dashboard:login')(
        user_passes_test(lambda u: u.is_active and u.is_staff, login_url='dashboard:login')(view)
    )


def _paginate(request, queryset, per_page=15):
    paginator = Paginator(queryset, per_page)
    page = paginator.get_page(request.GET.get('page'))
    return page


def _search(request, queryset, fields):
    query = (request.GET.get('q') or '').strip()
    if not query:
        return queryset, ''
    lookups = Q()
    for field in fields:
        lookups |= Q(**{f'{field}__icontains': query})
    return queryset.filter(lookups), query


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard:home')

    error = ''
    form = AdminLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user is not None and user.is_active and user.is_staff:
            login(request, user)
            return redirect(request.GET.get('next') or 'dashboard:home')
        error = "Login yoki parol noto'g'ri yoki sizda admin huquqlari yo'q."

    return render(request, 'dashboard/auth/login.html', {'form': form, 'error': error})


@login_required(login_url='dashboard:login')
def admin_logout(request):
    logout(request)
    return redirect('dashboard:login')


# ---------------------------------------------------------------------------
# Dashboard home
# ---------------------------------------------------------------------------

@staff_required
def home(request):
    now = timezone.now()
    last_30 = now - timedelta(days=30)
    last_60 = now - timedelta(days=60)

    enrollments_30 = UserCourse.objects.filter(enrolled_date__gte=last_30.date()).count()
    enrollments_prev_30 = UserCourse.objects.filter(
        enrolled_date__gte=last_60.date(), enrolled_date__lt=last_30.date()
    ).count()
    growth = 0
    if enrollments_prev_30:
        growth = round((enrollments_30 - enrollments_prev_30) * 100 / enrollments_prev_30, 1)

    stats = {
        'users_total': User.objects.count(),
        'users_active': User.objects.filter(is_active=True).count(),
        'centers_total': LearningCenter.objects.count(),
        'courses_total': Course.objects.count(),
        'blogs_total': BlogPost.objects.count(),
        'enrollments_total': UserCourse.objects.count(),
        'enrollments_30': enrollments_30,
        'enrollments_growth': growth,
        'contacts_total': ContactUs.objects.count(),
        'comments_total': UserCourseComment.objects.count(),
        'avg_rating': UserCourseRating.objects.aggregate(avg=Avg('rating'))['avg'] or 0,
    }

    revenue = Course.objects.aggregate(
        gross=Sum('price'),
        students=Sum('students_count'),
    )
    stats['revenue_potential'] = (revenue.get('gross') or 0) * (revenue.get('students') or 0) / max(stats['courses_total'], 1)

    chart_days = []
    chart_values = []
    for i in range(11, -1, -1):
        day = (now - timedelta(days=i * 7)).date()
        prev = day - timedelta(days=7)
        chart_days.append(day.strftime('%d %b'))
        chart_values.append(
            UserCourse.objects.filter(enrolled_date__gte=prev, enrolled_date__lt=day).count()
        )

    top_courses = (
        Course.objects.select_related('learning_center')
        .order_by('-students_count', '-rating')[:5]
    )
    top_centers = LearningCenter.objects.order_by('-students_count')[:5]
    recent_users = User.objects.order_by('-date_joined')[:6]
    recent_contacts = ContactUs.objects.order_by('-created_at')[:5]
    recent_comments = (
        UserCourseComment.objects.select_related('user', 'course')
        .order_by('-created_at')[:5]
    )

    category_distribution = list(
        Category.objects.annotate(c=Count('centers')).values('name', 'c').order_by('-c')[:6]
    )

    context = {
        'stats': stats,
        'chart_days': chart_days,
        'chart_values': chart_values,
        'top_courses': top_courses,
        'top_centers': top_centers,
        'recent_users': recent_users,
        'recent_contacts': recent_contacts,
        'recent_comments': recent_comments,
        'category_distribution': category_distribution,
        'page_title': 'Boshqaruv paneli',
        'breadcrumb': [{'label': 'Dashboard', 'url': None}],
    }
    return render(request, 'dashboard/home.html', context)


# ---------------------------------------------------------------------------
# Generic CRUD helpers (kept simple per-section so URLs stay readable)
# ---------------------------------------------------------------------------

def _delete_object(request, instance, redirect_to, message):
    if request.method == 'POST':
        instance.delete()
        messages.success(request, message)
        return redirect(redirect_to)
    return render(
        request,
        'dashboard/_confirm_delete.html',
        {'instance': instance, 'cancel_url': reverse(redirect_to)},
    )


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

@staff_required
def users_list(request):
    qs = User.objects.all().order_by('-date_joined')
    qs, query = _search(request, qs, ['username', 'first_name', 'last_name', 'email', 'phone_number'])
    role = request.GET.get('role')
    if role == 'staff':
        qs = qs.filter(is_staff=True)
    elif role == 'super':
        qs = qs.filter(is_superuser=True)
    elif role == 'inactive':
        qs = qs.filter(is_active=False)

    page = _paginate(request, qs)
    return render(request, 'dashboard/users/list.html', {
        'page': page,
        'query': query,
        'role': role or '',
        'page_title': 'Foydalanuvchilar',
        'breadcrumb': [{'label': 'Dashboard', 'url': reverse('dashboard:home')}, {'label': 'Foydalanuvchilar', 'url': None}],
    })


@staff_required
def users_form(request, pk=None):
    instance = get_object_or_404(User, pk=pk) if pk else None
    form = UserAdminForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Foydalanuvchi saqlandi.')
        return redirect('dashboard:users_list')

    return render(request, 'dashboard/users/form.html', {
        'form': form,
        'instance': instance,
        'page_title': 'Foydalanuvchini tahrirlash' if instance else 'Yangi foydalanuvchi',
        'breadcrumb': [
            {'label': 'Dashboard', 'url': reverse('dashboard:home')},
            {'label': 'Foydalanuvchilar', 'url': reverse('dashboard:users_list')},
            {'label': instance.username if instance else 'Yangi', 'url': None},
        ],
    })


@staff_required
def users_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "O'zingizni o'chira olmaysiz.")
        return redirect('dashboard:users_list')
    return _delete_object(request, user, 'dashboard:users_list', "Foydalanuvchi o'chirildi.")


# ---------------------------------------------------------------------------
# Instructor profiles
# ---------------------------------------------------------------------------

@staff_required
def instructors_list(request):
    qs = InstructorProfile.objects.select_related('user').order_by('-id')
    qs, query = _search(request, qs, ['title', 'user__username', 'user__email', 'location'])
    page = _paginate(request, qs)
    return render(request, 'dashboard/users/instructors_list.html', {
        'page': page,
        'query': query,
        'page_title': 'Instruktorlar',
        'breadcrumb': [{'label': 'Dashboard', 'url': reverse('dashboard:home')}, {'label': 'Instruktorlar', 'url': None}],
    })


@staff_required
def instructors_form(request, pk=None):
    instance = get_object_or_404(InstructorProfile, pk=pk) if pk else None
    form = InstructorProfileForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Instruktor profili saqlandi.')
        return redirect('dashboard:instructors_list')
    return render(request, 'dashboard/users/instructors_form.html', {
        'form': form,
        'instance': instance,
        'page_title': 'Instruktor profili',
        'breadcrumb': [
            {'label': 'Dashboard', 'url': reverse('dashboard:home')},
            {'label': 'Instruktorlar', 'url': reverse('dashboard:instructors_list')},
            {'label': str(instance) if instance else 'Yangi', 'url': None},
        ],
    })


@staff_required
def instructors_delete(request, pk):
    instance = get_object_or_404(InstructorProfile, pk=pk)
    return _delete_object(request, instance, 'dashboard:instructors_list', "Instruktor profili o'chirildi.")


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

@staff_required
def categories_list(request):
    qs = Category.objects.annotate(centers_count=Count('centers')).order_by('name')
    qs, query = _search(request, qs, ['name', 'description'])
    page = _paginate(request, qs)
    return render(request, 'dashboard/centers/categories_list.html', {
        'page': page,
        'query': query,
        'page_title': 'Kategoriyalar',
        'breadcrumb': [{'label': 'Dashboard', 'url': reverse('dashboard:home')}, {'label': 'Kategoriyalar', 'url': None}],
    })


@staff_required
def categories_form(request, pk=None):
    instance = get_object_or_404(Category, pk=pk) if pk else None
    form = CategoryForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Kategoriya saqlandi.')
        return redirect('dashboard:categories_list')
    return render(request, 'dashboard/centers/categories_form.html', {
        'form': form,
        'instance': instance,
        'page_title': 'Kategoriyani tahrirlash' if instance else 'Yangi kategoriya',
        'breadcrumb': [
            {'label': 'Dashboard', 'url': reverse('dashboard:home')},
            {'label': 'Kategoriyalar', 'url': reverse('dashboard:categories_list')},
            {'label': instance.name if instance else 'Yangi', 'url': None},
        ],
    })


@staff_required
def categories_delete(request, pk):
    instance = get_object_or_404(Category, pk=pk)
    return _delete_object(request, instance, 'dashboard:categories_list', "Kategoriya o'chirildi.")


# ---------------------------------------------------------------------------
# Learning Centers
# ---------------------------------------------------------------------------

@staff_required
def centers_list(request):
    qs = LearningCenter.objects.prefetch_related('categories').order_by('-id')
    qs, query = _search(request, qs, ['name', 'headline', 'description', 'location', 'email'])
    page = _paginate(request, qs)
    return render(request, 'dashboard/centers/list.html', {
        'page': page,
        'query': query,
        'page_title': "O'quv markazlari",
        'breadcrumb': [{'label': 'Dashboard', 'url': reverse('dashboard:home')}, {'label': "O'quv markazlari", 'url': None}],
    })


@staff_required
def centers_form(request, pk=None):
    instance = get_object_or_404(LearningCenter, pk=pk) if pk else None
    form = LearningCenterForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "O'quv markazi saqlandi.")
        return redirect('dashboard:centers_list')
    return render(request, 'dashboard/centers/form.html', {
        'form': form,
        'instance': instance,
        'page_title': "Markazni tahrirlash" if instance else "Yangi o'quv markazi",
        'breadcrumb': [
            {'label': 'Dashboard', 'url': reverse('dashboard:home')},
            {'label': "O'quv markazlari", 'url': reverse('dashboard:centers_list')},
            {'label': instance.name if instance else 'Yangi', 'url': None},
        ],
    })


@staff_required
def centers_delete(request, pk):
    instance = get_object_or_404(LearningCenter, pk=pk)
    return _delete_object(request, instance, 'dashboard:centers_list', "O'quv markazi o'chirildi.")


# ---------------------------------------------------------------------------
# Courses
# ---------------------------------------------------------------------------

@staff_required
def courses_list(request):
    qs = Course.objects.select_related('learning_center').order_by('-id')
    qs, query = _search(request, qs, ['name', 'subtitle', 'description', 'learning_center__name'])
    center_id = request.GET.get('center')
    if center_id:
        qs = qs.filter(learning_center_id=center_id)
    page = _paginate(request, qs)
    return render(request, 'dashboard/courses/list.html', {
        'page': page,
        'query': query,
        'centers': LearningCenter.objects.all().order_by('name'),
        'center_id': center_id or '',
        'page_title': 'Kurslar',
        'breadcrumb': [{'label': 'Dashboard', 'url': reverse('dashboard:home')}, {'label': 'Kurslar', 'url': None}],
    })


@staff_required
def courses_form(request, pk=None):
    instance = get_object_or_404(Course, pk=pk) if pk else None
    form = CourseForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Kurs saqlandi.')
        return redirect('dashboard:courses_list')
    return render(request, 'dashboard/courses/form.html', {
        'form': form,
        'instance': instance,
        'videos': instance.video_contents.all() if instance else None,
        'page_title': 'Kursni tahrirlash' if instance else 'Yangi kurs',
        'breadcrumb': [
            {'label': 'Dashboard', 'url': reverse('dashboard:home')},
            {'label': 'Kurslar', 'url': reverse('dashboard:courses_list')},
            {'label': instance.name if instance else 'Yangi', 'url': None},
        ],
    })


@staff_required
def courses_delete(request, pk):
    instance = get_object_or_404(Course, pk=pk)
    return _delete_object(request, instance, 'dashboard:courses_list', "Kurs o'chirildi.")


@staff_required
def videos_list(request):
    qs = VideoContent.objects.select_related('course').order_by('course', 'sort_order')
    qs, query = _search(request, qs, ['name', 'description', 'course__name'])
    page = _paginate(request, qs)
    return render(request, 'dashboard/courses/videos_list.html', {
        'page': page,
        'query': query,
        'page_title': 'Video darslar',
        'breadcrumb': [{'label': 'Dashboard', 'url': reverse('dashboard:home')}, {'label': 'Video darslar', 'url': None}],
    })


@staff_required
def videos_form(request, pk=None):
    instance = get_object_or_404(VideoContent, pk=pk) if pk else None
    form = VideoContentForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Video saqlandi.')
        return redirect('dashboard:videos_list')
    return render(request, 'dashboard/courses/videos_form.html', {
        'form': form,
        'instance': instance,
        'page_title': 'Videoni tahrirlash' if instance else 'Yangi video',
        'breadcrumb': [
            {'label': 'Dashboard', 'url': reverse('dashboard:home')},
            {'label': 'Video darslar', 'url': reverse('dashboard:videos_list')},
            {'label': instance.name if instance else 'Yangi', 'url': None},
        ],
    })


@staff_required
def videos_delete(request, pk):
    instance = get_object_or_404(VideoContent, pk=pk)
    return _delete_object(request, instance, 'dashboard:videos_list', "Video o'chirildi.")


# ---------------------------------------------------------------------------
# Blogs
# ---------------------------------------------------------------------------

@staff_required
def blogs_list(request):
    qs = BlogPost.objects.all().order_by('-published_at')
    qs, query = _search(request, qs, ['title', 'excerpt', 'content', 'topic', 'author_name'])
    featured = request.GET.get('featured')
    if featured == '1':
        qs = qs.filter(featured=True)
    page = _paginate(request, qs)
    return render(request, 'dashboard/blogs/list.html', {
        'page': page,
        'query': query,
        'featured': featured or '',
        'page_title': 'Blog yozuvlari',
        'breadcrumb': [{'label': 'Dashboard', 'url': reverse('dashboard:home')}, {'label': 'Blog', 'url': None}],
    })


@staff_required
def blogs_form(request, pk=None):
    instance = get_object_or_404(BlogPost, pk=pk) if pk else None
    form = BlogPostForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Blog saqlandi.')
        return redirect('dashboard:blogs_list')
    return render(request, 'dashboard/blogs/form.html', {
        'form': form,
        'instance': instance,
        'images': instance.images.all() if instance else None,
        'page_title': 'Blogni tahrirlash' if instance else 'Yangi blog',
        'breadcrumb': [
            {'label': 'Dashboard', 'url': reverse('dashboard:home')},
            {'label': 'Blog', 'url': reverse('dashboard:blogs_list')},
            {'label': instance.title if instance else 'Yangi', 'url': None},
        ],
    })


@staff_required
def blogs_delete(request, pk):
    instance = get_object_or_404(BlogPost, pk=pk)
    return _delete_object(request, instance, 'dashboard:blogs_list', "Blog o'chirildi.")


@staff_required
def blog_images_list(request):
    qs = BlogImage.objects.select_related('blog_post').order_by('-id')
    qs, query = _search(request, qs, ['blog_post__title', 'image_url'])
    page = _paginate(request, qs)
    return render(request, 'dashboard/blogs/images_list.html', {
        'page': page,
        'query': query,
        'page_title': 'Blog rasmlari',
        'breadcrumb': [{'label': 'Dashboard', 'url': reverse('dashboard:home')}, {'label': 'Blog rasmlari', 'url': None}],
    })


@staff_required
def blog_images_form(request, pk=None):
    instance = get_object_or_404(BlogImage, pk=pk) if pk else None
    form = BlogImageForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Rasm saqlandi.')
        return redirect('dashboard:blog_images_list')
    return render(request, 'dashboard/blogs/images_form.html', {
        'form': form,
        'instance': instance,
        'page_title': 'Rasmni tahrirlash' if instance else 'Yangi rasm',
        'breadcrumb': [
            {'label': 'Dashboard', 'url': reverse('dashboard:home')},
            {'label': 'Blog rasmlari', 'url': reverse('dashboard:blog_images_list')},
            {'label': str(instance) if instance else 'Yangi', 'url': None},
        ],
    })


@staff_required
def blog_images_delete(request, pk):
    instance = get_object_or_404(BlogImage, pk=pk)
    return _delete_object(request, instance, 'dashboard:blog_images_list', "Rasm o'chirildi.")


# ---------------------------------------------------------------------------
# Connections (enrollments / comments / ratings / testimonials / contacts)
# ---------------------------------------------------------------------------

@staff_required
def enrollments_list(request):
    qs = UserCourse.objects.select_related('user', 'course', 'course__learning_center').order_by('-enrolled_date')
    qs, query = _search(request, qs, ['user__username', 'user__email', 'course__name'])
    page = _paginate(request, qs)
    return render(request, 'dashboard/connections/enrollments_list.html', {
        'page': page,
        'query': query,
        'page_title': 'Kurs yozuvlari',
        'breadcrumb': [{'label': 'Dashboard', 'url': reverse('dashboard:home')}, {'label': 'Kurs yozuvlari', 'url': None}],
    })


@staff_required
def enrollments_delete(request, pk):
    instance = get_object_or_404(UserCourse, pk=pk)
    return _delete_object(request, instance, 'dashboard:enrollments_list', "Yozuv o'chirildi.")


@staff_required
def comments_list(request):
    qs = UserCourseComment.objects.select_related('user', 'course').order_by('-created_at')
    qs, query = _search(request, qs, ['text', 'user__username', 'course__name'])
    page = _paginate(request, qs)
    return render(request, 'dashboard/connections/comments_list.html', {
        'page': page,
        'query': query,
        'page_title': 'Sharhlar',
        'breadcrumb': [{'label': 'Dashboard', 'url': reverse('dashboard:home')}, {'label': 'Sharhlar', 'url': None}],
    })


@staff_required
def comments_delete(request, pk):
    instance = get_object_or_404(UserCourseComment, pk=pk)
    return _delete_object(request, instance, 'dashboard:comments_list', "Sharh o'chirildi.")


@staff_required
def ratings_list(request):
    qs = UserCourseRating.objects.select_related('user', 'course').order_by('-created_at')
    qs, query = _search(request, qs, ['user__username', 'course__name'])
    page = _paginate(request, qs)
    return render(request, 'dashboard/connections/ratings_list.html', {
        'page': page,
        'query': query,
        'page_title': 'Baholar',
        'breadcrumb': [{'label': 'Dashboard', 'url': reverse('dashboard:home')}, {'label': 'Baholar', 'url': None}],
    })


@staff_required
def ratings_delete(request, pk):
    instance = get_object_or_404(UserCourseRating, pk=pk)
    return _delete_object(request, instance, 'dashboard:ratings_list', "Baho o'chirildi.")


@staff_required
def testimonials_list(request):
    qs = Testimonial.objects.all().order_by('sort_order')
    qs, query = _search(request, qs, ['name', 'role', 'quote'])
    page = _paginate(request, qs)
    return render(request, 'dashboard/connections/testimonials_list.html', {
        'page': page,
        'query': query,
        'page_title': 'Tavsiyanomalar',
        'breadcrumb': [{'label': 'Dashboard', 'url': reverse('dashboard:home')}, {'label': 'Tavsiyanomalar', 'url': None}],
    })


@staff_required
def testimonials_form(request, pk=None):
    instance = get_object_or_404(Testimonial, pk=pk) if pk else None
    form = TestimonialForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Tavsiyanoma saqlandi.')
        return redirect('dashboard:testimonials_list')
    return render(request, 'dashboard/connections/testimonials_form.html', {
        'form': form,
        'instance': instance,
        'page_title': 'Tavsiyanomani tahrirlash' if instance else 'Yangi tavsiyanoma',
        'breadcrumb': [
            {'label': 'Dashboard', 'url': reverse('dashboard:home')},
            {'label': 'Tavsiyanomalar', 'url': reverse('dashboard:testimonials_list')},
            {'label': instance.name if instance else 'Yangi', 'url': None},
        ],
    })


@staff_required
def testimonials_delete(request, pk):
    instance = get_object_or_404(Testimonial, pk=pk)
    return _delete_object(request, instance, 'dashboard:testimonials_list', "Tavsiyanoma o'chirildi.")


@staff_required
def contacts_list(request):
    qs = ContactUs.objects.all().order_by('-created_at')
    qs, query = _search(request, qs, ['full_name', 'email', 'phone_number', 'message'])
    page = _paginate(request, qs)
    return render(request, 'dashboard/connections/contacts_list.html', {
        'page': page,
        'query': query,
        'page_title': "Murojaatlar",
        'breadcrumb': [{'label': 'Dashboard', 'url': reverse('dashboard:home')}, {'label': 'Murojaatlar', 'url': None}],
    })


@staff_required
def contacts_detail(request, pk):
    instance = get_object_or_404(ContactUs, pk=pk)
    form = ContactUsResponseForm(instance=instance)
    return render(request, 'dashboard/connections/contacts_detail.html', {
        'form': form,
        'instance': instance,
        'page_title': "Murojaat tafsiloti",
        'breadcrumb': [
            {'label': 'Dashboard', 'url': reverse('dashboard:home')},
            {'label': 'Murojaatlar', 'url': reverse('dashboard:contacts_list')},
            {'label': instance.full_name, 'url': None},
        ],
    })


@staff_required
def contacts_delete(request, pk):
    instance = get_object_or_404(ContactUs, pk=pk)
    return _delete_object(request, instance, 'dashboard:contacts_list', "Murojaat o'chirildi.")
