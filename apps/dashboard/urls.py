from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    # Auth
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),

    # Home / dashboard
    path('', views.home, name='home'),

    # Users
    path('users/', views.users_list, name='users_list'),
    path('users/new/', views.users_form, name='users_create'),
    path('users/<int:pk>/edit/', views.users_form, name='users_edit'),
    path('users/<int:pk>/delete/', views.users_delete, name='users_delete'),

    # Instructor profiles
    path('instructors/', views.instructors_list, name='instructors_list'),
    path('instructors/new/', views.instructors_form, name='instructors_create'),
    path('instructors/<int:pk>/edit/', views.instructors_form, name='instructors_edit'),
    path('instructors/<int:pk>/delete/', views.instructors_delete, name='instructors_delete'),

    # Categories
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/new/', views.categories_form, name='categories_create'),
    path('categories/<int:pk>/edit/', views.categories_form, name='categories_edit'),
    path('categories/<int:pk>/delete/', views.categories_delete, name='categories_delete'),

    # Centers
    path('centers/', views.centers_list, name='centers_list'),
    path('centers/new/', views.centers_form, name='centers_create'),
    path('centers/<int:pk>/edit/', views.centers_form, name='centers_edit'),
    path('centers/<int:pk>/delete/', views.centers_delete, name='centers_delete'),

    # Courses
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/new/', views.courses_form, name='courses_create'),
    path('courses/<int:pk>/edit/', views.courses_form, name='courses_edit'),
    path('courses/<int:pk>/delete/', views.courses_delete, name='courses_delete'),

    # Video contents
    path('videos/', views.videos_list, name='videos_list'),
    path('videos/new/', views.videos_form, name='videos_create'),
    path('videos/<int:pk>/edit/', views.videos_form, name='videos_edit'),
    path('videos/<int:pk>/delete/', views.videos_delete, name='videos_delete'),

    # Blogs
    path('blogs/', views.blogs_list, name='blogs_list'),
    path('blogs/new/', views.blogs_form, name='blogs_create'),
    path('blogs/<int:pk>/edit/', views.blogs_form, name='blogs_edit'),
    path('blogs/<int:pk>/delete/', views.blogs_delete, name='blogs_delete'),

    # Blog images
    path('blog-images/', views.blog_images_list, name='blog_images_list'),
    path('blog-images/new/', views.blog_images_form, name='blog_images_create'),
    path('blog-images/<int:pk>/edit/', views.blog_images_form, name='blog_images_edit'),
    path('blog-images/<int:pk>/delete/', views.blog_images_delete, name='blog_images_delete'),

    # Enrollments
    path('enrollments/', views.enrollments_list, name='enrollments_list'),
    path('enrollments/<int:pk>/delete/', views.enrollments_delete, name='enrollments_delete'),

    # Comments
    path('comments/', views.comments_list, name='comments_list'),
    path('comments/<int:pk>/delete/', views.comments_delete, name='comments_delete'),

    # Ratings
    path('ratings/', views.ratings_list, name='ratings_list'),
    path('ratings/<int:pk>/delete/', views.ratings_delete, name='ratings_delete'),

    # Testimonials
    path('testimonials/', views.testimonials_list, name='testimonials_list'),
    path('testimonials/new/', views.testimonials_form, name='testimonials_create'),
    path('testimonials/<int:pk>/edit/', views.testimonials_form, name='testimonials_edit'),
    path('testimonials/<int:pk>/delete/', views.testimonials_delete, name='testimonials_delete'),

    # Contacts
    path('contacts/', views.contacts_list, name='contacts_list'),
    path('contacts/<int:pk>/', views.contacts_detail, name='contacts_detail'),
    path('contacts/<int:pk>/delete/', views.contacts_delete, name='contacts_delete'),
]
