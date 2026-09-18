from django.test import TestCase
from django.urls import reverse
from centers.models import Category, LearningCenter
from courses.models import Course, VideoContent
from users.models import InstructorProfile, User


class TeacherAccessTests(TestCase):
    def test_legacy_admin_login_uses_public_login(self):
        self.assertRedirects(self.client.get(reverse('dashboard:login')), reverse('login'))

    def test_admin_login_returns_to_requested_dashboard(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.url, reverse('login') + '?next=' + reverse('dashboard:home'))
        response = self.client.post(reverse('login'), {'username': 'owner', 'password': 'test-secret', 'next': reverse('dashboard:home')})
        self.assertRedirects(response, reverse('dashboard:home'))

    def test_public_login_rejects_external_redirect(self):
        response = self.client.post(reverse('login'), {'username': 'owner', 'password': 'test-secret', 'next': 'https://example.com/'})
        self.assertEqual(response.url, reverse('profile') + '?lang=uz')

    def test_teacher_home_redirects_to_shared_profile(self):
        self.client.force_login(self.teacher)
        self.assertRedirects(self.client.get(reverse('teacher:home')), reverse('profile'))

    def test_student_profile_has_no_course_management(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse('profile'))
        self.assertNotContains(response, reverse('teacher:course_create'))

    def test_admin_can_create_teacher_role(self):
        from dashboard.forms import UserAdminForm
        form = UserAdminForm(data={'username': 'newteacher', 'password': 'test-secret', 'is_active': True, 'is_teacher': True})
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertTrue(InstructorProfile.objects.filter(user=user).exists())
        self.assertFalse(user.is_staff)

    def test_teacher_course_form_uses_shared_header(self):
        self.client.force_login(self.teacher)
        response = self.client.get(reverse('teacher:course_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, reverse('profile'))

    @classmethod
    def setUpTestData(cls):
        cls.teacher = User.objects.create_user('teacher', password='test-secret')
        cls.other = User.objects.create_user('other', password='test-secret')
        cls.student = User.objects.create_user('student', password='test-secret')
        cls.admin = User.objects.create_superuser('owner', password='test-secret')
        cls.profile = InstructorProfile.objects.create(user=cls.teacher, title='Designer', bio='Bio', mission='Teach')
        cls.other_profile = InstructorProfile.objects.create(user=cls.other, title='SMM', bio='Bio', mission='Teach')
        cls.center = LearningCenter.objects.create(name='Academy', slug='academy', description='Courses', phone_number='+998901234567')
        cls.category = Category.objects.get(slug='design')
        cls.course = Course.objects.create(name='Design', slug='design', description='Course', learning_center=cls.center, instructor=cls.profile)
        cls.foreign = Course.objects.create(name='SMM', slug='smm', description='Course', learning_center=cls.center, instructor=cls.other_profile)
        cls.lesson = VideoContent.objects.create(course=cls.foreign, name='Foreign lesson', video_url='https://example.com/video')

    def test_student_cannot_access_teacher_portal(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(reverse('teacher:home')).status_code, 403)

    def test_teacher_sees_only_own_courses(self):
        self.client.force_login(self.teacher)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['teaching_page']), [self.course])
        self.assertTemplateUsed(response, 'base.html')
        self.assertNotContains(response, 'teacher:home')

    def test_foreign_objects_are_inaccessible(self):
        self.client.force_login(self.teacher)
        for name, pk in [('course_edit', self.foreign.pk), ('course_delete', self.foreign.pk), ('lesson_edit', self.lesson.pk), ('lesson_delete', self.lesson.pk)]:
            self.assertEqual(self.client.post(reverse('teacher:' + name, args=[pk]), {}).status_code, 404)
        self.assertTrue(Course.objects.filter(pk=self.foreign.pk).exists())

    def test_teacher_cannot_access_admin_even_if_staff(self):
        self.teacher.is_staff = True
        self.teacher.save()
        self.client.force_login(self.teacher)
        for name in ['home', 'users_create', 'instructors_create', 'courses_list']:
            self.assertEqual(self.client.get(reverse('dashboard:' + name)).status_code, 302)

    def test_create_course_ignores_forged_owner_and_featured(self):
        self.client.force_login(self.teacher)
        response = self.client.post(reverse('teacher:course_create'), {
            'name': 'Frontend', 'description': 'Build interfaces', 'learning_center': self.center.pk,
            'category': self.category.pk, 'price': 0, 'instructor': self.other_profile.pk, 'featured': 'on',
        })
        self.assertEqual(response.status_code, 302)
        course = Course.objects.get(name='Frontend')
        self.assertEqual(course.instructor, self.profile)
        self.assertFalse(course.featured)

    def test_lesson_cannot_be_moved_to_foreign_course(self):
        self.client.force_login(self.teacher)
        response = self.client.post(reverse('teacher:lesson_create', args=[self.course.pk]), {
            'name': 'Intro', 'description': 'Introduction', 'video_url': 'https://example.com/intro',
            'sort_order': 0, 'course': self.foreign.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(VideoContent.objects.get(name='Intro').course, self.course)

    def test_deletion_requires_post_and_profile_revocation_blocks_access(self):
        self.client.force_login(self.teacher)
        self.assertEqual(self.client.get(reverse('teacher:course_delete', args=[self.course.pk])).status_code, 405)
        self.profile.delete()
        self.assertEqual(self.client.get(reverse('teacher:home')).status_code, 403)

    def test_superadmin_can_open_instructor_form(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse('dashboard:instructors_create')).status_code, 200)

    def test_catalog_filters_by_category(self):
        self.course.category = self.category
        self.course.save()
        response = self.client.get(reverse('course_catalog'), {'category': 'design'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['page']), [self.course])

    def test_course_without_instructor_renders(self):
        self.course.instructor = None
        self.course.save()
        self.assertEqual(self.client.get(reverse('course_detail', args=[self.course.slug])).status_code, 200)
