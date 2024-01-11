from django.db import models
from django.utils.text import slugify

from centers.models import LearningCenter
from connections.models import UserCourseRating, UserCourseComment


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='course_images/')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        ratings = UserCourseRating.objects.filter(course=self)
        if ratings:
            self.rating = sum([rating.rating for rating in ratings]) / len(ratings)
            self.save()
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    @property
    def comments(self):
        return UserCourseComment.objects.filter(course=self)

    def __str__(self):
        return f'{self.learning_center} - {self.name}'


class VideoContent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='video_images/')
    video_url = models.URLField()

    def __str__(self):
        return f'{self.course} - {self.name}'
