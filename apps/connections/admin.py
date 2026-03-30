from django.contrib import admin

from connections.models import Testimonial, UserCourse, UserCourseComment, UserCourseRating


@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_date')
    search_fields = ('user__username', 'course__name')


@admin.register(UserCourseComment)
class UserCourseCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    search_fields = ('user__username', 'course__name', 'text')


@admin.register(UserCourseRating)
class UserCourseRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    search_fields = ('user__username', 'course__name')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'sort_order')
    search_fields = ('name', 'role', 'quote')
