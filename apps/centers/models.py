from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify

regex_phone_number = RegexValidator(
    r'^\+998\d{9,15}$',
    message="Phone number must be in the format +998XXXXXXXXX, where X is a digit."
)


class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class LearningCenter(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    location = models.CharField(max_length=128)
    email = models.EmailField()
    phone_number = models.CharField(max_length=17, unique=True, validators=[regex_phone_number])
    image = models.URLField(blank=True)
    website = models.URLField(blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

