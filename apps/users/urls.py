from django.urls import path

from .views import user_login, user_logout, user_signup, profile_page, edit_profile

urlpatterns = [

    path('register/', user_signup, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path("profile/", profile_page, name="profile"),
    path("edit_profile/", edit_profile, name="edit_profile")
]
