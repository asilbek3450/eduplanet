from django.urls import path, include


urlpatterns = [
    path('', include('blogs.urls')),
    path('centers/', include('centers.urls')),
    path('courses/', include('courses.urls')),
    path('users/', include('users.urls')),
    path('connections/', include('connections.urls')),
]
