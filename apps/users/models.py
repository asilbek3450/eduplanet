from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


regex_phone_number = RegexValidator(
    r'^\+998\d{9,15}$',
    message="Phone number must be in the format +998XXXXXXXXX, where X is a digit."
)


class User(AbstractUser):
    phone_number = models.CharField(max_length=17, unique=True, validators=[regex_phone_number], blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        return self.username


class ContactUs(models.Model):
    full_name = models.CharField(max_length=128)
    email = models.EmailField()
    phone_number = models.CharField(max_length=17, validators=[regex_phone_number])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
