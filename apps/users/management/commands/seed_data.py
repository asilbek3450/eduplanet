"""
Management command: python manage.py seed_data

To'liq realistik ma'lumotlar bilan bazani to'ldiradi:
  - O'zbek nomli 20 ta student
  - Kurs ro'yxatga yozilishlar (enrollments)
  - Realistik o'zbek tilidagi izohlar
  - Kurs reytinglari
"""

import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from connections.models import UserCourse, UserCourseComment, UserCourseRating
from courses.models import Course
from site_content import ensure_platform_content

User = get_user_model()

# ---------------------------------------------------------------------------
# Ma'lumotlar
# ---------------------------------------------------------------------------

STUDENTS = [
    {"first_name": "Dilshod",    "last_name": "Qodirov",    "username": "dilshod_qodirov",    "email": "dilshod@example.uz",    "phone": "+998901234567"},
    {"first_name": "Madina",     "last_name": "Karimova",   "username": "madina_karimova",    "email": "madina@example.uz",     "phone": "+998901234568"},
    {"first_name": "Azizbek",    "last_name": "Juraev",     "username": "azizbek_juraev",     "email": "azizbek@example.uz",    "phone": "+998901234569"},
    {"first_name": "Zulfiya",    "last_name": "Nazarova",   "username": "zulfiya_nazarova",   "email": "zulfiya@example.uz",    "phone": "+998901234570"},
    {"first_name": "Bobur",      "last_name": "Toshmatov",  "username": "bobur_toshmatov",    "email": "bobur@example.uz",      "phone": "+998901234571"},
    {"first_name": "Shahlo",     "last_name": "Yusupova",   "username": "shahlo_yusupova",    "email": "shahlo@example.uz",     "phone": "+998901234572"},
    {"first_name": "Jasur",      "last_name": "Mirzayev",   "username": "jasur_mirzayev",     "email": "jasur@example.uz",      "phone": "+998901234573"},
    {"first_name": "Nilufar",    "last_name": "Xolmatova",  "username": "nilufar_xolmatova",  "email": "nilufar@example.uz",    "phone": "+998901234574"},
    {"first_name": "Otabek",     "last_name": "Rашидов",    "username": "otabek_rashidov",    "email": "otabek@example.uz",     "phone": "+998901234575"},
    {"first_name": "Kamola",     "last_name": "Ibragimova", "username": "kamola_ibragimova",  "email": "kamola@example.uz",     "phone": "+998901234576"},
    {"first_name": "Sardor",     "last_name": "Hamidov",    "username": "sardor_hamidov",     "email": "sardor@example.uz",     "phone": "+998901234577"},
    {"first_name": "Gulnora",    "last_name": "Abdullayeva","username": "gulnora_abdullayeva","email": "gulnora@example.uz",    "phone": "+998901234578"},
    {"first_name": "Ulugbek",    "last_name": "Sobirov",    "username": "ulugbek_sobirov",    "email": "ulugbek@example.uz",    "phone": "+998901234579"},
    {"first_name": "Feruza",     "last_name": "Tursunova",  "username": "feruza_tursunova",   "email": "feruza@example.uz",     "phone": "+998901234580"},
    {"first_name": "Shohruh",    "last_name": "Ergashev",   "username": "shohruh_ergashev",   "email": "shohruh@example.uz",    "phone": "+998901234581"},
    {"first_name": "Dildora",    "last_name": "Mahmudova",  "username": "dildora_mahmudova",  "email": "dildora@example.uz",    "phone": "+998901234582"},
    {"first_name": "Firdavs",    "last_name": "Ismoilov",   "username": "firdavs_ismoilov",   "email": "firdavs@example.uz",    "phone": "+998901234583"},
    {"first_name": "Munira",     "last_name": "Holiqova",   "username": "munira_holiqova",    "email": "munira@example.uz",     "phone": "+998901234584"},
    {"first_name": "Sherzod",    "last_name": "Xasanov",    "username": "sherzod_xasanov",    "email": "sherzod@example.uz",    "phone": "+998901234585"},
    {"first_name": "Malika",     "last_name": "Rahimova",   "username": "malika_rahimova",    "email": "malika@example.uz",     "phone": "+998901234586"},
]

# Kurs sluglari bo'yicha izohlar ro'yxati
COMMENTS_BY_COURSE = {
    "python-for-beginners-uzbekistan": [
        ("dilshod_qodirov",    5, "Bu kurs menga Python ni tushunishga juda yordam berdi. Asilbek aka tushuntirishlar juda tushunarli va amaliy. Expense tracker loyihasini qilganimda birinchi marta kodim ishlaganda juda xursand bo'ldim!"),
        ("madina_karimova",    5, "O'zbek tilida shu darajadagi sifatli kurs topish qiyin edi. Har bir mavzu ketma-ket va mantiqiy tarzda tushuntirilgan. API bilan ishlash moduli ayniqsa foydali bo'ldi."),
        ("azizbek_juraev",     4, "Kurs mazmuni a'lo, lekin ba'zi mashqlar bir oz qiyin tuyuldi. Umuman olganda Python asoslarini yaxshi o'rgandim va hozir Django kursiga o'tdim."),
        ("zulfiya_nazarova",   5, "Boshlovchi sifatida bu kurs menga ideal start berdi. Telegram parser loyihasini qilganimda do'stlarimga ham ko'rsatdim - ular ham hayron qoldi!"),
        ("bobur_toshmatov",    5, "3 oydan buyon Python o'rganmoqchi edim, lekin boshqa kurslar tushunarsiz edi. Bu kurs hammasini o'zgartirdi. Rahmat Asilbek aka!"),
        ("shahlo_yusupova",    4, "Juda yaxshi kurs. Functions va modules qismi ayniqsa chuqur tushuntirilgan. GitHub ga loyiha qo'yishni ham o'rgandim."),
        ("jasur_mirzayev",     5, "Real proyektlar orqali o'rganish usuli juda samarali. Faqat nazariya emas, amaliyot ham ko'p. Backend yo'liga o'tish uchun ideal tayyorlov."),
        ("shohruh_ergashev",   5, "Python kurslarini ko'p ko'rdim, lekin bu kurs boshqacha. Har bir darsda biror narsa qurasan. GitHub portfolio ochishga yordam berdi."),
    ],
    "django-fullstack-mastery": [
        ("sardor_hamidov",     5, "Django Fullstack kursi haqiqatdan ham professional darajada. Auth system, dashboard va SaaS arxitekturasi bilan ishlash tajribam sezilarli oshdi."),
        ("ulugbek_sobirov",    5, "Bu kursni tugatgach birinchi freelance loyihamni oldim. Kurs davomida o'rganilgan authentication va permission tizimi haqiqiy loyihada darhol kerak bo'ldi."),
        ("feruza_tursunova",   4, "Kurs hajmi katta, lekin har bir modul o'z o'rnida. PostgreSQL bilan ishlash qismi ayniqsa foydali. Bir oz vaqt talab qiladi, lekin arziydi."),
        ("shohruh_ergashev",   5, "SaaS billing dashboard qurishni bu kursda o'rgandim. Endi o'z startupim uchun backend yozmoqdaman. Asilbek akaning kod yozish uslubi juda clean."),
        ("dildora_mahmudova",  5, "Fullstack yo'nalishda eng to'liq kurs bu. Admin panel, API va template ham bor. Birinchi haftadanoq ishlatishni boshlayapsiz."),
        ("kamola_ibragimova",  4, "Background tasks va email notification qismini o'rganish juda foydali bo'ldi. Real startup backlogiga o'xshash tasklar tufayli ishga tayyorlik oshdi."),
        ("otabek_rashidov",    5, "Django ORM chuqurligi va custom admin panel bo'limini ayniqsa yoqdim. Bu kurs boshqa Django kurslardan ancha ustun."),
    ],
    "rest-api-with-drf": [
        ("firdavs_ismoilov",   5, "DRF bo'yicha o'zbek tilida shu darajadagi kurs topilmaydi. ViewSet, serializer va permission tizimi chuqur tushuntirilgan. Rahmat!"),
        ("sherzod_xasanov",    5, "API documentation va versioning bo'limini ayniqsa yoqdim. Frontendchilar bilan ishlashda bu bilimlar juda kerak bo'lmoqda."),
        ("malika_rahimova",    4, "Throttling va caching mavzulari juda qiziq bo'ldi. Ba'zi advanced qismlar uchun Django Fullstack kursini oldindan o'tish tavsiya etiladi."),
        ("munira_holiqova",    5, "JWT auth va refresh token mexanizmini bu kursda yaxshi tushundim. Mobile app backend uchun ideal bilimlar."),
        ("otabek_rashidov",    5, "3-chi haftadanoq real API yozib, Postman da test qilayotgan edim. Amaliy yondashuv kuchli. Ishga kirish uchun kerakli barcha API pattern larni o'rgandim."),
        ("ulugbek_sobirov",    5, "DRF bilan React frontend ni ulash qismini ko'rsatgani juda qimmatli. CORS, token va response format - hammasi aniq tushuntirilgan."),
        ("jasur_mirzayev",     4, "Kurs juda foydali. Nested serializer va writable M2M field larni qanday qilishni aniq tushundim. Kamchiligi: video sifati ba'zan past."),
    ],
    "web-development-bootcamp-django": [
        ("madina_karimova",    5, "HTML, CSS va Django ni birgalikda o'rganish g'oyasi juda to'g'ri. Landing page dan to Django template gacha ketma-ket. Ajoyib kurs!"),
        ("shahlo_yusupova",    5, "Tailwind CSS integratsiyasi va responsive design qismlari juda amaliy. Portfolio uchun 2 ta tugallangan loyiha qildim."),
        ("nilufar_xolmatova",  4, "JavaScript asoslari bo'limi tezroq o'tilib, ko'proq Django ga e'tibor qaratilsa yaxshi bo'lardi. Lekin umuman olganda juda yaxshi kurs."),
    ],
    "postgresql-for-developers": [
        ("sardor_hamidov",     5, "PostgreSQL indexing va query optimization bo'limi meni hayron qoldirdi. Django ORM yetarli emas - raw SQL va EXPLAIN ANALYZE ham kerak ekan."),
        ("ulugbek_sobirov",    4, "Window functions va CTE larni bu kursda o'rgandim. Murakkab reporting querylarini endi osongina yozmoqdaman."),
        ("sherzod_xasanov",    5, "Django da N+1 muammo va select_related/prefetch_related larni bu kursdan keyin to'liq tushundim. Har bir backend developer ko'rishi kerak."),
    ],
    "clean-code-in-python": [
        ("firdavs_ismoilov",   5, "SOLID principles va design patterns ni bu kursda Python tilida ko'rish juda foydali bo'ldi. Kod sifatim sezilarli oshdi."),
        ("dildora_mahmudova",  5, "Service layer va repository pattern larni o'rganib, loyihamni to'liq qayta tuzillashtirdim. Code review da endi ko'proq baho olmoqdaman."),
        ("kamola_ibragimova",  4, "Unit test va mocking qismi juda amaliy. Lekin async Python bo'limi biroz qisqa edi. Keyingi versiyada chuqurroq bo'lsa yaxshi."),
    ],
    "devops-basics-for-python-engineers": [
        ("bobur_toshmatov",    5, "Docker va CI/CD ni bu kursdan oldin qo'rqib ishlatardim. Hozir GitHub Actions bilan har kuni ishlayman. Juda amaliy kurs!"),
        ("sardor_hamidov",     4, "Railway va Render deployment qismi juda foydali. Environment management va logs bilan ishlash odatim shakllandi."),
        ("jasur_mirzayev",     5, "Django loyihani productonga chiqarish uchun zarur barcha bilimlar bu kursda bor. Monitoring va alerting bo'limi ayniqsa qiziq."),
        ("azizbek_juraev",     5, "Nginx + Gunicorn + Docker Compose stack ni bu kursda to'liq o'zgartirdim. Endi ishonch bilan deploy qila olaman."),
    ],
    "data-science-foundations-python": [
        ("nilufar_xolmatova",  5, "Data analysis bo'yicha o'zbek tilida kurs yo'q deb o'ylardim. Bu kurs ajoyib. Pandas va visualization orqali real dataset tahlil qildim."),
        ("gulnora_abdullayeva",4, "Kurs juda foydali, ayniqsa EDA va storytelling qismi. Lekin SQL integratsiyasi ko'proq bo'lsa yaxshi bo'lardi."),
        ("zulfiya_nazarova",   5, "Analytics va reporting workflow ni bu kursda o'rgandim. Endi kompaniyadagi hisobotlarni Python bilan qilmoqdaman."),
        ("munira_holiqova",    4, "Matplotlib va Seaborn bilan vizualizatsiya qilishni o'rganish qiziqarli bo'ldi. Keyingi qadam: machine learning yo'nalishi."),
    ],
}

# Enrollments - kim qaysi kursga yozilgan
ENROLLMENTS = {
    "dilshod_qodirov":    ["python-for-beginners-uzbekistan", "django-fullstack-mastery"],
    "madina_karimova":    ["python-for-beginners-uzbekistan", "web-development-bootcamp-django"],
    "azizbek_juraev":     ["python-for-beginners-uzbekistan", "rest-api-with-drf", "devops-basics-for-python-engineers"],
    "zulfiya_nazarova":   ["python-for-beginners-uzbekistan", "data-science-foundations-python"],
    "bobur_toshmatov":    ["python-for-beginners-uzbekistan", "devops-basics-for-python-engineers"],
    "shahlo_yusupova":    ["python-for-beginners-uzbekistan", "web-development-bootcamp-django"],
    "jasur_mirzayev":     ["python-for-beginners-uzbekistan", "rest-api-with-drf", "devops-basics-for-python-engineers"],
    "nilufar_xolmatova":  ["data-science-foundations-python", "web-development-bootcamp-django"],
    "otabek_rashidov":    ["rest-api-with-drf", "django-fullstack-mastery"],
    "kamola_ibragimova":  ["django-fullstack-mastery", "clean-code-in-python"],
    "sardor_hamidov":     ["django-fullstack-mastery", "devops-basics-for-python-engineers", "postgresql-for-developers"],
    "gulnora_abdullayeva":["data-science-foundations-python"],
    "ulugbek_sobirov":    ["django-fullstack-mastery", "rest-api-with-drf", "postgresql-for-developers"],
    "feruza_tursunova":   ["django-fullstack-mastery"],
    "shohruh_ergashev":   ["django-fullstack-mastery", "python-for-beginners-uzbekistan"],
    "dildora_mahmudova":  ["django-fullstack-mastery", "clean-code-in-python"],
    "firdavs_ismoilov":   ["rest-api-with-drf", "clean-code-in-python"],
    "munira_holiqova":    ["rest-api-with-drf", "data-science-foundations-python"],
    "sherzod_xasanov":    ["rest-api-with-drf", "postgresql-for-developers"],
    "malika_rahimova":    ["rest-api-with-drf"],
}


class Command(BaseCommand):
    help = "Bazani realistik ma'lumotlar bilan to'ldiradi (foydalanuvchilar, enrollments, izohlar, reytinglar)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Avval mavjud student, enrollment, izoh va reytinglarni o\'chiradi',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("EduPlanet ma'lumotlarini to'ldirish boshlandi..."))

        # Avval asosiy kontentni (kurslar, markazlar, bloglar) seed qilamiz
        self.stdout.write("  → Asosiy platforma kontenti tekshirilmoqda...")
        ensure_platform_content()
        self.stdout.write(self.style.SUCCESS("  ✓ Platforma kontenti tayyor"))

        with transaction.atomic():
            if options['reset']:
                self._reset_student_data()

            users = self._create_students()
            self._create_enrollments(users)
            self._create_comments_and_ratings(users)
            self._update_course_stats()

        self.stdout.write(self.style.SUCCESS("\nBarcha ma'lumotlar muvaffaqiyatli qo'shildi!"))
        self._print_summary()

    def _reset_student_data(self):
        self.stdout.write("  → Mavjud student ma'lumotlari o'chirilmoqda...")
        usernames = [s["username"] for s in STUDENTS]
        students = User.objects.filter(username__in=usernames)
        UserCourseComment.objects.filter(user__in=students).delete()
        UserCourseRating.objects.filter(user__in=students).delete()
        UserCourse.objects.filter(user__in=students).delete()
        students.delete()
        self.stdout.write(self.style.WARNING("  ✓ Eski student ma'lumotlari o'chirildi"))

    def _create_students(self):
        self.stdout.write("  → Studentlar yaratilmoqda...")
        users = {}
        created_count = 0
        for data in STUDENTS:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name":  data["last_name"],
                    "email":      data["email"],
                    "phone_number": data["phone"],
                },
            )
            if created:
                user.set_password("Student!2026")
                user.save(update_fields=["password"])
                created_count += 1
            users[data["username"]] = user

        self.stdout.write(self.style.SUCCESS(f"  ✓ {created_count} ta yangi student, {len(users) - created_count} ta mavjud"))
        return users

    def _create_enrollments(self, users):
        self.stdout.write("  → Kursga yozilishlar yaratilmoqda...")
        courses = {c.slug: c for c in Course.objects.all()}
        enrollment_count = 0
        base_date = date.today() - timedelta(days=90)

        for username, slugs in ENROLLMENTS.items():
            user = users.get(username)
            if not user:
                continue
            for i, slug in enumerate(slugs):
                course = courses.get(slug)
                if not course:
                    self.stdout.write(self.style.WARNING(f"    ! Kurs topilmadi: {slug}"))
                    continue
                _, created = UserCourse.objects.get_or_create(user=user, course=course)
                if created:
                    # enrolled_date ni past qilib o'rnatish uchun to'g'ridan update
                    delta_days = random.randint(0, 80)
                    UserCourse.objects.filter(user=user, course=course).update(
                        enrolled_date=base_date + timedelta(days=delta_days)
                    )
                    enrollment_count += 1

        self.stdout.write(self.style.SUCCESS(f"  ✓ {enrollment_count} ta yangi enrollment"))

    def _create_comments_and_ratings(self, users):
        self.stdout.write("  → Izohlar va reytinglar yaratilmoqda...")
        courses = {c.slug: c for c in Course.objects.all()}
        comment_count = 0
        rating_count = 0

        for slug, entries in COMMENTS_BY_COURSE.items():
            course = courses.get(slug)
            if not course:
                self.stdout.write(self.style.WARNING(f"    ! Kurs topilmadi: {slug}"))
                continue

            for username, rating_val, text in entries:
                user = users.get(username)
                if not user:
                    continue

                # Faqat ro'yxatdan o'tgan foydalanuvchi izoh qoldira oladi
                if not UserCourse.objects.filter(user=user, course=course).exists():
                    continue

                _, c_created = UserCourseComment.objects.get_or_create(
                    user=user,
                    course=course,
                    defaults={"text": text},
                )
                if c_created:
                    comment_count += 1

                _, r_created = UserCourseRating.objects.get_or_create(
                    user=user,
                    course=course,
                    defaults={"rating": rating_val},
                )
                if r_created:
                    rating_count += 1

        self.stdout.write(self.style.SUCCESS(f"  ✓ {comment_count} ta izoh, {rating_count} ta reyting"))

    def _update_course_stats(self):
        self.stdout.write("  → Kurs statistikalari yangilanmoqda...")
        for course in Course.objects.all():
            enrollment_count = UserCourse.objects.filter(course=course).count()
            if enrollment_count > 0:
                Course.objects.filter(pk=course.pk).update(students_count=enrollment_count)
            course.refresh_from_db()
            course.update_rating()

        self.stdout.write(self.style.SUCCESS("  ✓ Kurs statistikalari yangilandi"))

    def _print_summary(self):
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.MIGRATE_HEADING("YAKUNIY STATISTIKA"))
        self.stdout.write("=" * 50)
        self.stdout.write(f"  Foydalanuvchilar:  {User.objects.count()} ta")
        self.stdout.write(f"  Kategoriyalar:     {__import__('centers').models.Category.objects.count()} ta")
        self.stdout.write(f"  Markazlar:         {__import__('centers').models.LearningCenter.objects.count()} ta")
        self.stdout.write(f"  Kurslar:           {Course.objects.count()} ta")
        self.stdout.write(f"  Enrollments:       {UserCourse.objects.count()} ta")
        self.stdout.write(f"  Izohlar:           {UserCourseComment.objects.count()} ta")
        self.stdout.write(f"  Reytinglar:        {UserCourseRating.objects.count()} ta")
        self.stdout.write(f"  Blog postlar:      {__import__('blogs').models.BlogPost.objects.count()} ta")
        self.stdout.write(f"  Testimoniallar:    {__import__('connections').models.Testimonial.objects.count()} ta")
        self.stdout.write("=" * 50)
        self.stdout.write(self.style.SUCCESS("\nStudent login: username / Student!2026"))
