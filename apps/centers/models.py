from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify

regex_phone_number = RegexValidator(
    r'^\+998\d{9,15}$',
    message='Phone number must be in the format +998XXXXXXXXX, where X is a digit.'
)


class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=32, blank=True)
    translations = models.JSONField(default=dict, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class LearningCenter(models.Model):
    name = models.CharField(max_length=128)
    headline = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='centers')
    location = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=17, unique=True, validators=[regex_phone_number])
    image = models.URLField(blank=True)
    website = models.URLField(blank=True)
    students_count = models.PositiveIntegerField(default=0)
    mentors_count = models.PositiveIntegerField(default=0)
    courses_count = models.PositiveIntegerField(default=0)
    features = models.JSONField(default=list, blank=True)
    translations = models.JSONField(default=dict, blank=True)
    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.seo_title:
            self.seo_title = self.name
        if not self.seo_description:
            self.seo_description = self.description[:160]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
