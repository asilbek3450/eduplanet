from django.contrib import admin

from centers.models import Category, LearningCenter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(LearningCenter)
class LearningCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'students_count', 'mentors_count', 'courses_count')
    list_filter = ('categories',)
    search_fields = ('name', 'headline', 'description', 'location')
    prepopulated_fields = {'slug': ('name',)}
