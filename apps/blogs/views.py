from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from site_content import (
    get_blog_detail_context,
    get_blog_list_context,
    get_homepage_context,
    get_language,
    with_lang,
)
from users.forms import ContactUsForm
from .models import BlogPost


def dashboard(request):
    lang = get_language(request)
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Xabaringiz muvaffaqiyatli yuborildi.")
            return redirect(with_lang('/users/success/', lang))
        messages.error(request, "Iltimos, formadagi ma'lumotlarni tekshirib qayta yuboring.")
    else:
        form = ContactUsForm()

    context = get_homepage_context(request)
    context['form'] = form
    return render(request, template_name='index.html', context=context)


def blog_list(request):
    context = get_blog_list_context(request)
    per_page = getattr(settings, 'BLOG_POSTS_PER_PAGE', 9)
    paginator = Paginator(context['blogs'], per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context['blogs'] = page_obj
    context['page_obj'] = page_obj
    context['paginator'] = paginator
    return render(request, template_name='blogs/blog_list.html', context=context)


def blog_detail(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    context = get_blog_detail_context(request, blog)
    return render(request, template_name='blogs/blog_detail.html', context=context)
