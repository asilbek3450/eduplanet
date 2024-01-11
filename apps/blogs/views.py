from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from users.forms import ContactUsForm
from .models import BlogPost, BlogImage


# Create your views here.

def dashboard(request):
    last_blog = BlogPost.objects.last()
    last_blog_cover_image_url = BlogImage.objects.filter(blog_post=last_blog).last().image_url
    other_latest_three_blogs = BlogPost.objects.all().order_by('-created_at')[1:4]

    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            print('message sent successfully', form.cleaned_data)
            # send notification to user via dashboard
            messages.success(request, 'Xabar yuborildi')
            return redirect('contact_us_success')
    else:
        form = ContactUsForm()
        messages.error(request, 'Xabar yuborishda xatolik yuz berdi')

    context = {
        'last_blog': last_blog,
        'last_blog_cover_image_url': last_blog_cover_image_url,
        'three_blogs': other_latest_three_blogs,
        'form': form
    }
    return render(request, template_name='index.html', context=context)


def blog_list(request):
    blogs = BlogPost.objects.all().order_by('-created_at')
    context = {
        'blogs': blogs
    }
    return render(request, template_name='blogs/blog_list.html', context=context)


def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    cover_image = BlogImage.objects.filter(blog_post=blog).first()
    blog_images = BlogImage.objects.filter(blog_post=blog)
    context = {
        'blog': blog,
        'cover_image': cover_image,
        'blog_images': blog_images
    }
    return render(request, template_name='blogs/blog_detail.html', context=context)