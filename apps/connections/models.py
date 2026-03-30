from django.db import models

from users.models import User


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    enrolled_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user} - {self.course}'


class UserCourseComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment: {self.text} | by {self.user.username} - for {self.course.name}'


class UserCourseRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'RATING: {self.rating} | by {self.user.username} - for {self.course.name}'


class Testimonial(models.Model):
    name = models.CharField(max_length=128)
    role = models.CharField(max_length=160)
    quote = models.TextField()
    avatar_url = models.URLField(blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    sort_order = models.PositiveIntegerField(default=0)
    translations = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name
