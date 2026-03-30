from django.contrib import admin

from courses.models import Course, VideoContent


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'learning_center', 'level', 'students_count', 'rating', 'featured')
    list_filter = ('learning_center', 'level', 'featured')
    search_fields = ('name', 'subtitle', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'duration', 'is_preview', 'sort_order')
    list_filter = ('is_preview', 'course')
    search_fields = ('name', 'description', 'course__name')
