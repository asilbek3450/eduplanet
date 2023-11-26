import string

from django.db import models

# Create your models here.

# class Courses for Learning Center Courses and their details with youtube video links


CATEGORY_CHOICES = (
    ('programming', 'Programming'),
    ('robotics', 'Robotics'),
    ('design', 'Design'),
    ('language', 'Language'),
    ('kids', 'Kids'),
)


# class Learning Center for the students
class LearningCenter(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=128, choices=CATEGORY_CHOICES)

    location = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(max_length=128)
    website = models.URLField(max_length=128)

    def __str__(self):
        return f'{self.name} - {self.description}'


class Courses(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    youtube_link = models.URLField(max_length=128)
    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.description}'


class Post(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.description}'
