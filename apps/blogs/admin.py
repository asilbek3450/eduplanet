from django.contrib import admin

from blogs.models import BlogImage, BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'published_at', 'featured')
    list_filter = ('featured', 'topic')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ('blog_post', 'image_url')
    search_fields = ('blog_post__title', 'image_url')
