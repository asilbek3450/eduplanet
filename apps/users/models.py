from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


regex_phone_number = RegexValidator(
    r'^\+998\d{9,15}$',
    message='Phone number must be in the format +998XXXXXXXXX, where X is a digit.'
)


class User(AbstractUser):
    phone_number = models.CharField(max_length=17, unique=True, validators=[regex_phone_number], blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.phone_number:
            self.phone_number = self.phone_number.replace(' ', '')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    title = models.CharField(max_length=180)
    bio = models.TextField()
    mission = models.TextField()
    profile_description = models.TextField(blank=True)
    experience_years = models.PositiveSmallIntegerField(default=5)
    skills = models.JSONField(default=list, blank=True)
    location = models.CharField(max_length=128, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    telegram = models.URLField(blank=True)
    avatar_url = models.URLField(blank=True)
    translations = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class ContactUs(models.Model):
    full_name = models.CharField(max_length=128)
    email = models.EmailField()
    phone_number = models.CharField(max_length=17, validators=[regex_phone_number])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
