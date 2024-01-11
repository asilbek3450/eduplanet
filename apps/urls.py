from django.urls import path, include

from blogs.views import dashboard

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('centers/', include('centers.urls')),
    path('courses/', include('courses.urls')),
    path('users/', include('users.urls'))
]
