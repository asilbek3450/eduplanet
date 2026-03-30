from django.contrib import admin

from users.models import ContactUs, InstructorProfile, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    ordering = ('-id',)


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'experience_years', 'location')
    search_fields = ('user__username', 'user__email', 'title', 'bio')


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number', 'message')
