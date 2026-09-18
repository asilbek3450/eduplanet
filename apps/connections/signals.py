from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Avg
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from courses.models import Course
from .models import UserCourse, UserCourseRating


def refresh_student_count(course_id):
    """Keep the denormalized display counter equal to actual enrollments."""
    count = UserCourse.objects.filter(course_id=course_id).count()
    Course.objects.filter(pk=course_id).update(students_count=count)


def refresh_course_rating(course_id):
    """Persist a one-decimal average immediately after every review change."""
    average = UserCourseRating.objects.filter(course_id=course_id).aggregate(Avg('rating'))['rating__avg']
    value = Decimal('0.0') if average is None else Decimal(str(average)).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP
    )
    Course.objects.filter(pk=course_id).update(rating=value)


@receiver(post_save, sender=UserCourse)
def update_student_count_on_enrollment(sender, instance, **kwargs):
    refresh_student_count(instance.course_id)


@receiver(post_delete, sender=UserCourse)
def update_student_count_on_unenrollment(sender, instance, **kwargs):
    refresh_student_count(instance.course_id)


@receiver(post_save, sender=UserCourseRating)
def update_rating_on_save(sender, instance, **kwargs):
    refresh_course_rating(instance.course_id)


@receiver(post_delete, sender=UserCourseRating)
def update_rating_on_delete(sender, instance, **kwargs):
    refresh_course_rating(instance.course_id)
