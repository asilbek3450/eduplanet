from django.db import models
from django.db.models import Avg
from django.utils.text import slugify

from centers.models import LearningCenter


class Course(models.Model):
    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, related_name='courses')
    image = models.URLField(blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, db_index=True)
    level = models.CharField(max_length=32, blank=True)
    duration = models.CharField(max_length=32, blank=True)
    lessons_count = models.PositiveIntegerField(default=0)
    students_count = models.PositiveIntegerField(default=0)
    hours_watched = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    highlights = models.JSONField(default=list, blank=True)
    outcomes = models.JSONField(default=list, blank=True)
    curriculum = models.JSONField(default=list, blank=True)
    translations = models.JSONField(default=dict, blank=True)
    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    featured = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-students_count', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.seo_title:
            self.seo_title = self.name
        if not self.seo_description:
            self.seo_description = self.description[:160]

        if self.pk:
            avg = (
                self.__class__._default_manager
                .using(self._state.db)
                .filter(pk=self.pk)
                .values_list('pk', flat=True)
                .first()
            )
            # Use a separate query to avoid self-reference issues
            from connections.models import UserCourseRating
            result = UserCourseRating.objects.filter(course_id=self.pk).aggregate(avg=Avg('rating'))
            if result['avg'] is not None:
                self.rating = round(result['avg'], 1)

        super().save(*args, **kwargs)

    def update_rating(self):
        from connections.models import UserCourseRating
        result = UserCourseRating.objects.filter(course=self).aggregate(avg=Avg('rating'))
        self.rating = round(result['avg'], 1) if result['avg'] is not None else 0
        Course.objects.filter(pk=self.pk).update(rating=self.rating)

    @property
    def comments(self):
        from connections.models import UserCourseComment
        return UserCourseComment.objects.select_related('user').filter(course=self).order_by('-created_at')

    def __str__(self):
        return f'{self.learning_center} - {self.name}'


class VideoContent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='video_contents')
    cover_image = models.URLField(blank=True)
    video_url = models.URLField()
    duration = models.CharField(max_length=32, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f'{self.course} - {self.name}'
