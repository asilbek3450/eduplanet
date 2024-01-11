from django.contrib import admin

from connections.models import UserCourse, UserCourseComment, UserCourseRating

# Register your models here.

admin.site.register(UserCourse)
admin.site.register(UserCourseComment)
admin.site.register(UserCourseRating)
