from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from centers.models import LearningCenter
from courses.models import Course
from users.models import User

from .models import UserCourse, UserCourseRating


class CourseMetricsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='learner', password='safe-password')
        self.center = LearningCenter.objects.create(
            name='Test center', description='Test description', location='Tashkent',
            email='test@example.com', phone_number='+998901234567',
        )
        self.course = Course.objects.create(
            name='Test course', description='Test description', learning_center=self.center,
        )

    def test_enrollment_is_post_only_and_updates_student_count(self):
        self.client.force_login(self.user)
        url = reverse('enroll_course', args=[self.course.pk])

        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(self.client.post(url).status_code, 302)

        self.course.refresh_from_db()
        self.assertEqual(self.course.students_count, 1)

    def test_rating_is_unique_validated_and_updates_course_average(self):
        rating = UserCourseRating.objects.create(user=self.user, course=self.course, rating=5)
        self.course.refresh_from_db()
        self.assertEqual(self.course.rating, 5)

        another_user = User.objects.create_user(username='learner-two', password='safe-password')
        UserCourseRating.objects.create(user=another_user, course=self.course, rating=4)
        self.course.refresh_from_db()
        self.assertEqual(self.course.rating, 4.5)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                UserCourseRating.objects.create(user=self.user, course=self.course, rating=3)

        invalid_rating = UserCourseRating(user=self.user, course=self.course, rating=6)
        with self.assertRaises(ValidationError):
            invalid_rating.full_clean()

        rating.delete()
        self.course.refresh_from_db()
        self.assertEqual(self.course.rating, 4)

# Create your tests here.
