from django.contrib import admin

from users.models import User, ContactUs


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-id',)


admin.site.register(User, UserAdmin)
admin.site.register(ContactUs)
