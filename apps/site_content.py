import json
from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse

from blogs.models import BlogImage, BlogPost
from centers.models import Category, LearningCenter
from connections.models import Testimonial, UserCourse
from courses.models import Course, VideoContent
from users.models import InstructorProfile


LANGUAGE_OPTIONS = {
    "uz": "O'zbekcha",
    "en": "English",
    "ru": "Русский",
}
LANGUAGE_META = {
    "uz": {
        "label": "O'zbekcha",
        "short": "UZ",
        "native": "O'zbekcha",
        "flag_alt": "Uzbekistan flag",
        "flag_svg": (
            "<svg viewBox='0 0 60 40' xmlns='http://www.w3.org/2000/svg' aria-hidden='true' focusable='false'>"
            "<rect width='60' height='13.34' y='0' fill='#0099B5'/>"
            "<rect width='60' height='1' y='13.34' fill='#CE1126'/>"
            "<rect width='60' height='12.34' y='14.34' fill='#FFFFFF'/>"
            "<rect width='60' height='1' y='26.68' fill='#CE1126'/>"
            "<rect width='60' height='12.32' y='27.68' fill='#1EB53A'/>"
            "<g fill='#FFFFFF'>"
            "<circle cx='14' cy='7' r='3.4'/>"
            "<circle cx='15.4' cy='7' r='3.4' fill='#0099B5'/>"
            "<circle cx='20' cy='4.5' r='0.5'/><circle cx='22.4' cy='4.5' r='0.5'/>"
            "<circle cx='20' cy='7' r='0.5'/><circle cx='22.4' cy='7' r='0.5'/><circle cx='24.8' cy='7' r='0.5'/>"
            "<circle cx='20' cy='9.5' r='0.5'/><circle cx='22.4' cy='9.5' r='0.5'/><circle cx='24.8' cy='9.5' r='0.5'/><circle cx='27.2' cy='9.5' r='0.5'/>"
            "</g>"
            "</svg>"
        ),
    },
    "en": {
        "label": "English",
        "short": "EN",
        "native": "English",
        "flag_alt": "United Kingdom flag",
        "flag_svg": (
            "<svg viewBox='0 0 60 40' xmlns='http://www.w3.org/2000/svg' aria-hidden='true' focusable='false'>"
            "<rect width='60' height='40' fill='#012169'/>"
            "<path d='M0 0 L60 40 M60 0 L0 40' stroke='#FFFFFF' stroke-width='8'/>"
            "<path d='M0 0 L60 40' stroke='#C8102E' stroke-width='4'/>"
            "<path d='M60 0 L0 40' stroke='#C8102E' stroke-width='4'/>"
            "<path d='M30 0 V40 M0 20 H60' stroke='#FFFFFF' stroke-width='10'/>"
            "<path d='M30 0 V40 M0 20 H60' stroke='#C8102E' stroke-width='6'/>"
            "</svg>"
        ),
    },
    "ru": {
        "label": "Русский",
        "short": "RU",
        "native": "Русский",
        "flag_alt": "Russia flag",
        "flag_svg": (
            "<svg viewBox='0 0 60 40' xmlns='http://www.w3.org/2000/svg' aria-hidden='true' focusable='false'>"
            "<rect width='60' height='13.34' y='0' fill='#FFFFFF'/>"
            "<rect width='60' height='13.34' y='13.34' fill='#0039A6'/>"
            "<rect width='60' height='13.32' y='26.68' fill='#D52B1E'/>"
            "</svg>"
        ),
    },
}
DEFAULT_LANGUAGE = "uz"
GLOBAL_KEYWORDS = [
    "Python course Uzbekistan",
    "Django course online",
    "Backend course Tashkent",
    "Asilbek Mirolimov",
]

UI_COPY = {
    "uz": {
        "home": "Bosh sahifa",
        "courses": "Kurslar",
        "centers": "Markazlar",
        "blog": "Blog",
        "about": "Asilbek haqida",
        "contact": "Bog'lanish",
        "login": "Kirish",
        "register": "Ro'yxatdan o'tish",
        "profile": "Profil",
        "logout": "Chiqish",
        "hero_badge": "Senior Software Engineer и преподаватель",
        "hero_title": "Backend karyerangizni real product tajriba bilan boshlang",
        "hero_description": "EduPlanet - bu Asilbek Mirolimovning amaliy tajribaga tayangan LMS platformasi. Bu yerda siz Python, Django, REST API, PostgreSQL va DevOps asoslarini real startup workflow orqali o'rganasiz.",
        "hero_primary_cta": "Kurslarni ko'rish",
        "hero_secondary_cta": "Bepul roadmap olish",
        "stats_students": "Faol talabalar",
        "stats_courses": "Yopiq va ochiq kurslar",
        "stats_rating": "O'rtacha baho",
        "stats_hours": "Ko'rilgan soatlar",
        "featured_courses": "Eng talabgir kurslar",
        "featured_courses_description": "Boshlovchilar, junior backend developerlar va product-minded muhandislar uchun ishlab chiqilgan amaliy kurslar.",
        "instructor_title": "Asilbek Mirolimov bilan o'rganing",
        "testimonials_title": "Natijalar gapiradi",
        "blog_title": "SEO va karyera blogi",
        "blog_description": "Python course Uzbekistan, Django course online va Backend course Tashkent kabi qidiruvlar uchun foydali, chuqur va amaliy maqolalar.",
        "cta_title": "Start your programming journey today",
        "cta_description": "Bir kurs bilan boshlang, real portfolio yig'ing va ishga tayyor developerga aylanish uchun tizimli yo'lni tanlang.",
        "cta_primary": "Bugun boshlash",
        "cta_secondary": "Maslahat olish",
        "contact_title": "Savolingiz bormi? Birga yechamiz.",
        "contact_description": "Kurs tanlash, learning path yoki jamoa uchun korporativ training bo'yicha 24 soat ichida javob beramiz.",
        "sticky_primary": "Kurslar",
        "sticky_secondary": "Bog'lanish",
        "newsletter_label": "Haftalik backend insights",
        "students_label": "talaba",
        "lessons_label": "dars",
        "hours_label": "soat",
        "level_label": "Daraja",
        "duration_label": "Davomiyligi",
        "read_article": "Maqolani o'qish",
        "enroll": "Kursga yozilish",
        "curriculum": "Nimalarni o'rganasiz",
        "results": "Kurs yakunida natijalar",
        "preview_lessons": "Preview darslar",
        "center_courses": "Markazdagi kurslar",
        "back_home": "Bosh sahifaga qaytish",
        "featured_badge": "Launch-ready LMS",
        "meta_site_name": "EduPlanet | Python, Django va Backend kurslari",
        "contact_success_title": "Xabaringiz qabul qilindi",
        "contact_success_description": "Rahmat. Odatda 1 ish kuni ichida siz bilan bog'lanamiz.",
    },
    "en": {
        "home": "Home",
        "courses": "Courses",
        "centers": "Centers",
        "blog": "Blog",
        "about": "About Asilbek",
        "contact": "Contact",
        "login": "Login",
        "register": "Register",
        "profile": "Profile",
        "logout": "Logout",
        "hero_badge": "Senior Software Engineer & Educator",
        "hero_title": "Build a backend career with real product experience",
        "hero_description": "EduPlanet is Asilbek Mirolimov's practical LMS platform where you learn Python, Django, REST API, PostgreSQL, and DevOps fundamentals through real startup workflows.",
        "hero_primary_cta": "Explore courses",
        "hero_secondary_cta": "Get free roadmap",
        "stats_students": "Active students",
        "stats_courses": "Courses and bootcamps",
        "stats_rating": "Average rating",
        "stats_hours": "Hours watched",
        "featured_courses": "Featured courses",
        "featured_courses_description": "Hands-on programs for beginners, junior backend developers, and product-minded engineers.",
        "instructor_title": "Learn with Asilbek Mirolimov",
        "testimonials_title": "Outcomes that feel real",
        "blog_title": "SEO and career blog",
        "blog_description": "Practical articles designed for high-intent searches like Python course Uzbekistan, Django course online, and Backend course Tashkent.",
        "cta_title": "Start your programming journey today",
        "cta_description": "Begin with one course, build a real portfolio, and follow a structured path toward becoming a job-ready developer.",
        "cta_primary": "Start today",
        "cta_secondary": "Talk to us",
        "contact_title": "Need help choosing your learning path?",
        "contact_description": "We reply within 24 hours for course guidance, roadmap questions, or team training requests.",
        "sticky_primary": "Courses",
        "sticky_secondary": "Contact",
        "newsletter_label": "Weekly backend insights",
        "students_label": "students",
        "lessons_label": "lessons",
        "hours_label": "hours",
        "level_label": "Level",
        "duration_label": "Duration",
        "read_article": "Read article",
        "enroll": "Enroll now",
        "curriculum": "What you will cover",
        "results": "Learning outcomes",
        "preview_lessons": "Preview lessons",
        "center_courses": "Courses in this center",
        "back_home": "Back to homepage",
        "featured_badge": "Launch-ready LMS",
        "meta_site_name": "EduPlanet | Python, Django and Backend Courses",
        "contact_success_title": "Your message is in",
        "contact_success_description": "Thanks. We usually get back within one business day.",
    },
    "ru": {
        "home": "Главная",
        "courses": "Курсы",
        "centers": "Направления",
        "blog": "Блог",
        "about": "Об Асилбеке",
        "contact": "Контакты",
        "login": "Войти",
        "register": "Регистрация",
        "profile": "Профиль",
        "logout": "Выйти",
        "hero_badge": "Senior Software Engineer & Educator",
        "hero_title": "Стройте backend-карьеру на основе реального product-опыта",
        "hero_description": "EduPlanet — практическая LMS-платформа Асилбека Миролимова, где вы изучаете Python, Django, REST API, PostgreSQL и основы DevOps через реальные startup-workflow.",
        "hero_primary_cta": "Смотреть курсы",
        "hero_secondary_cta": "Получить дорожную карту",
        "stats_students": "Активные студенты",
        "stats_courses": "Курсы и буткемпы",
        "stats_rating": "Средний рейтинг",
        "stats_hours": "Часы просмотра",
        "featured_courses": "Популярные курсы",
        "featured_courses_description": "Практичные программы для новичков, junior backend-разработчиков и product-minded инженеров.",
        "instructor_title": "Учитесь с Асилбеком Миролимовым",
        "testimonials_title": "Результаты говорят сами за себя",
        "blog_title": "SEO и карьерный блог",
        "blog_description": "Глубокие и практичные статьи для высокоинтентных запросов: Python course Uzbekistan, Django course online и Backend course Tashkent.",
        "cta_title": "Начните свой путь в программировании уже сегодня",
        "cta_description": "Начните с одного курса, соберите реальное портфолио и двигайтесь по системному пути к уровню job-ready разработчика.",
        "cta_primary": "Начать сейчас",
        "cta_secondary": "Получить консультацию",
        "contact_title": "Есть вопрос? Разберем вместе.",
        "contact_description": "Отвечаем в течение 24 часов по выбору курса, roadmap или корпоративному обучению.",
        "sticky_primary": "Курсы",
        "sticky_secondary": "Контакты",
        "newsletter_label": "Еженедельные backend-инсайты",
        "students_label": "студентов",
        "lessons_label": "уроков",
        "hours_label": "часов",
        "level_label": "Уровень",
        "duration_label": "Длительность",
        "read_article": "Читать статью",
        "enroll": "Записаться",
        "curriculum": "Программа курса",
        "results": "Результаты обучения",
        "preview_lessons": "Открытые уроки",
        "center_courses": "Курсы в этом направлении",
        "back_home": "На главную",
        "featured_badge": "LMS, готовая к запуску",
        "meta_site_name": "EduPlanet | Курсы по Python, Django и backend-разработке",
        "contact_success_title": "Сообщение отправлено",
        "contact_success_description": "Спасибо. Обычно мы отвечаем в течение одного рабочего дня.",
    },
}

HOME_EXTRAS = {
    "uz": {
        "trust_strip": [
            "Real SaaS case studylar",
            "Weekly mentor review",
            "Portfolio-first yondashuv",
            "SEO va product thinking",
            "Uzbek + English tech terminology",
        ],
        "momentum_label": "Platform momentum",
        "momentum_title": "Talabalar faqat dars ko'rmaydi - ular har hafta productga yaqin natija chiqaradi",
        "momentum_description": "Onboardingdan keyin har bir learner uchun aniq sprint ritmi, code review nuqtasi va progress ko'rinadigan deliverable mavjud.",
        "recent_activity": [
            {
                "name": "Dilshod Qodirov",
                "role": "Junior Backend Developer",
                "action": "REST API modulida token auth va throttlingni ishlab, GitHub portfolio projectini yangiladi.",
                "time": "12 min oldin",
                "metric": "2 commit + 1 review",
            },
            {
                "name": "Madina Karimova",
                "role": "Computer Science student",
                "action": "Python fundamentals trackni tugatib, expense tracker mini-projectini deploy qildi.",
                "time": "47 min oldin",
                "metric": "1 live project",
            },
            {
                "name": "Azizbek Juraev",
                "role": "Freelance developer",
                "action": "Django Fullstack Mastery ichida billing-ready dashboard flowini yakunladi.",
                "time": "1 soat oldin",
                "metric": "4.9 mentor score",
            },
            {
                "name": "Elena Sokolova",
                "role": "Product analyst",
                "action": "Data-oriented reporting workflowdan foydalanib, birinchi analytics case study yozdi.",
                "time": "Bugun",
                "metric": "3 insight cards",
            },
        ],
        "platform_pillars": [
            {
                "stat": "7 kun",
                "title": "Tez onboarding",
                "description": "Birinchi haftadayoq sizga mos learning path, tavsiya etilgan kurs va amaliy tasklar beriladi.",
            },
            {
                "stat": "2-3 build",
                "title": "Har haftalik sprint",
                "description": "Nazariya darhol mini build, refactor yoki API task bilan mustahkamlanadi.",
            },
            {
                "stat": "24 soat",
                "title": "Mentor feedback window",
                "description": "Uy vazifasi va savollar bo'yicha qisqa, aniq va productga yaqin tavsiyalar olinadi.",
            },
        ],
        "journey_label": "Learning flywheel",
        "journey_title": "Platforma o'qishni emas, transformatsiyani dizayn qiladi",
        "journey_description": "Har bir bosqich real muammo, real output va keyingi qadamga tayyor signal bilan yakunlanadi.",
        "journey_steps": [
            {
                "step": "01",
                "title": "Diagnostic start",
                "description": "Darajangiz, maqsadingiz va vaqt rejimingizga qarab eng to'g'ri track tanlanadi.",
            },
            {
                "step": "02",
                "title": "Build sprint",
                "description": "Kurs moduli ichida landing page, API, dashboard yoki DB tasklar orqali skill mustahkamlanadi.",
            },
            {
                "step": "03",
                "title": "Review loop",
                "description": "Kod sifati, naming, UX va architecture bo'yicha qisqa feedback bilan natija yaxshilanadi.",
            },
            {
                "step": "04",
                "title": "Launch outcome",
                "description": "GitHub-ready loyiha, portfolio case study yoki interviewga tayyor bo'ladigan deliverable chiqadi.",
            },
        ],
        "experience_label": "Learning experience",
        "experience_title": "Bir platformada kurs, mentor va career signalini birlashtirdik",
        "experience_description": "Quyidagi rejimlar birgalikda ishlaganda EduPlanet oddiy LMS emas, balki o'sish tizimiga aylanadi.",
        "experience_modes": [
            {
                "id": "sprint",
                "label": "Build sprintlar",
                "metric": "Haftasiga 2-3 amaliy build",
                "headline": "Nazariya darhol ishlab ko'riladigan delivery flowga aylanadi",
                "description": "Har kurs ichida real product tasklar bor: auth flow, API endpoint, responsive section, analytics query yoki deploy checklist.",
                "bullets": [
                    "Lessondan keyin darhol output beradigan task",
                    "Portfolio uchun yig'ilib boradigan real deliverable",
                    "Product mindset va clean execution birga o'sadi",
                ],
            },
            {
                "id": "review",
                "label": "Code review loop",
                "metric": "Naming, UX va architecture feedback",
                "headline": "Faqat ishlaydigan kod emas - tushunarli va professional yechim quriladi",
                "description": "Studentlar qayerda chalkashayotganini tez ko'rish uchun kod, copy va layout qarorlari bo'yicha soddalashtirilgan review mantiqi qo'shilgan.",
                "bullets": [
                    "Kodni tozalash va qayta tashkil qilish odati",
                    "Readable API va maintainable template yondashuvi",
                    "Junior darajadan product-minded engineer darajasiga o'tish",
                ],
            },
            {
                "id": "career",
                "label": "Career upgrade",
                "metric": "Roadmap, portfolio va confidence",
                "headline": "Har bir track ishga tayyorlikni ko'rsatadigan signal bilan yakunlanadi",
                "description": "Faqat kursni bitirish emas, balki GitHub, case study, interview talking points va next-step clarity ham beriladi.",
                "bullets": [
                    "Portfolio positioning uchun aniq yo'l-yo'riq",
                    "Freelance yoki ishga kirish uchun kerakli proof-of-work",
                    "Nimani keyin o'rganish kerakligi bo'yicha aniq navbat",
                ],
            },
        ],
        "path_label": "Path finder",
        "path_title": "Hozir qaysi yo'ldan boshlasangiz, natija tezroq keladi?",
        "path_description": "Maqsadingizga mos yo'lni tanlang - platforma sizni mos kurs va markazga olib kiradi.",
        "path_primary": "Tavsiya etilgan kurs",
        "path_secondary": "Markaz haqida",
        "goal_paths": [
            {
                "id": "starter",
                "label": "Noldan boshlayman",
                "headline": "Tushunarli start va tez confidence uchun Python fundamentals + web context",
                "description": "Agar siz hali dasturlashga endi kirayotgan bo'lsangiz, birinchi maqsad - syntax emas, o'rganishni davom ettira oladigan ishonch yig'ish.",
                "bullets": [
                    "Python syntaxni qo'rqmasdan ishlata boshlaysiz",
                    "Birinchi mini projectlar bilan GitHub portfelingiz ochiladi",
                    "Keyingi Django yoki web trackga tabiiy o'tasiz",
                ],
                "course_slug": "python-for-beginners-uzbekistan",
                "center_slug": "web-development",
            },
            {
                "id": "backend",
                "label": "Backendga o'taman",
                "headline": "Django, auth, dashboard va product architecture bilan professional backend yo'li",
                "description": "Agar fundamentals bor, lekin real tizim qanday yig'ilishini chuqur ko'rmoqchi bo'lsangiz, bu eng tez value beradigan route.",
                "bullets": [
                    "Productionga yaqin SaaS arxitekturasini ko'rasiz",
                    "API, database va access control birgalikda ishlashini tushunasiz",
                    "Interview va freelance uchun kuchli signal yig'asiz",
                ],
                "course_slug": "django-fullstack-mastery",
                "center_slug": "backend-engineering",
            },
            {
                "id": "api",
                "label": "API specialist bo'laman",
                "headline": "Frontend, mobile va third-party integratsiyalar uchun ishonchli endpointlar yozish",
                "description": "Agar siz product backend ichida aynan API qatlamini mustahkamlashni istasangiz, bu yo'l sizni tezda amaliy darajaga olib chiqadi.",
                "bullets": [
                    "DRF patterns va resource modelingni mustahkamlaysiz",
                    "Permissions, docs va predictable error flow bilan ishlaysiz",
                    "Team collaboration uchun tayyor contractlar yozishni o'rganasiz",
                ],
                "course_slug": "rest-api-with-drf",
                "center_slug": "backend-engineering",
            },
        ],
        "blog_spotlight_label": "Editor pick",
    },
    "en": {
        "trust_strip": [
            "Real SaaS case studies",
            "Weekly mentor review",
            "Portfolio-first learning",
            "SEO and product thinking",
            "Uzbek + English tech terminology",
        ],
        "momentum_label": "Platform momentum",
        "momentum_title": "Students do not just watch lessons - they ship visible progress every week",
        "momentum_description": "After onboarding, each learner moves through clear sprints, review points, and output that can be shown publicly.",
        "recent_activity": [
            {
                "name": "Dilshod Qodirov",
                "role": "Junior Backend Developer",
                "action": "Finished token auth and throttling in the REST API track and refreshed his GitHub portfolio project.",
                "time": "12 min ago",
                "metric": "2 commits + 1 review",
            },
            {
                "name": "Madina Karimova",
                "role": "Computer Science student",
                "action": "Completed the Python fundamentals track and deployed her expense tracker mini-project.",
                "time": "47 min ago",
                "metric": "1 live project",
            },
            {
                "name": "Azizbek Juraev",
                "role": "Freelance developer",
                "action": "Wrapped the billing-ready dashboard flow inside Django Fullstack Mastery.",
                "time": "1 hour ago",
                "metric": "4.9 mentor score",
            },
            {
                "name": "Elena Sokolova",
                "role": "Product analyst",
                "action": "Published her first analytics case study using the data reporting workflow.",
                "time": "Today",
                "metric": "3 insight cards",
            },
        ],
        "platform_pillars": [
            {
                "stat": "7 days",
                "title": "Fast onboarding",
                "description": "You get a tailored path, recommended course stack, and practical tasks in your very first week.",
            },
            {
                "stat": "2-3 builds",
                "title": "Weekly sprint rhythm",
                "description": "Theory is reinforced immediately through mini builds, refactors, or API tasks.",
            },
            {
                "stat": "24 hours",
                "title": "Mentor feedback window",
                "description": "Assignments and questions receive short, practical, product-minded feedback.",
            },
        ],
        "journey_label": "Learning flywheel",
        "journey_title": "The platform is designed for transformation, not passive watching",
        "journey_description": "Every stage ends with a real problem solved, a visible output, and a clear next step.",
        "journey_steps": [
            {"step": "01", "title": "Diagnostic start", "description": "We match your level, goals, and pace to the right starting track."},
            {"step": "02", "title": "Build sprint", "description": "Each module turns into a landing page, API, dashboard, database task, or deploy step."},
            {"step": "03", "title": "Review loop", "description": "Code quality, naming, UX, and architecture get improved through concise feedback."},
            {"step": "04", "title": "Launch outcome", "description": "You leave with GitHub-ready work, a portfolio case study, or interview-ready talking points."},
        ],
        "experience_label": "Learning experience",
        "experience_title": "We combine course content, mentor guidance, and career signal in one flow",
        "experience_description": "Together these modes make EduPlanet feel closer to a growth system than a generic LMS.",
        "experience_modes": [
            {
                "id": "sprint",
                "label": "Build sprints",
                "metric": "2-3 practical builds each week",
                "headline": "Theory turns into a delivery flow you can immediately practice",
                "description": "Each course includes real product tasks such as auth flows, API endpoints, responsive sections, analytics queries, or deploy checklists.",
                "bullets": [
                    "Tasks that create output right after the lesson",
                    "Portfolio deliverables that compound over time",
                    "Product thinking and clean execution grow together",
                ],
            },
            {
                "id": "review",
                "label": "Code review loop",
                "metric": "Naming, UX, and architecture feedback",
                "headline": "You build solutions that are not only working, but professional and readable",
                "description": "A simplified review layer highlights confusing code, weak copy, or shaky layout decisions before they become habits.",
                "bullets": [
                    "A stronger instinct for cleanup and refactoring",
                    "Readable APIs and maintainable templates",
                    "A clear bridge from junior output to product-minded engineering",
                ],
            },
            {
                "id": "career",
                "label": "Career upgrade",
                "metric": "Roadmap, portfolio, and confidence",
                "headline": "Each track ends with a signal that proves you are ready for the next step",
                "description": "Beyond course completion, you get GitHub positioning, case study direction, interview talking points, and clarity about what to learn next.",
                "bullets": [
                    "Practical guidance for portfolio positioning",
                    "Proof-of-work for freelance or hiring conversations",
                    "A clear order for the next skills to learn",
                ],
            },
        ],
        "path_label": "Path finder",
        "path_title": "Which route gives you the fastest momentum right now?",
        "path_description": "Choose the goal that sounds most like you and the platform will surface the best course and center.",
        "path_primary": "Recommended course",
        "path_secondary": "About the center",
        "goal_paths": [
            {
                "id": "starter",
                "label": "Starting from zero",
                "headline": "Build confidence first with Python fundamentals and web context",
                "description": "If you are new to programming, the first win is not syntax alone - it is building enough confidence to keep going.",
                "bullets": [
                    "Use Python syntax without fear",
                    "Open your GitHub portfolio with first mini-projects",
                    "Move naturally into Django or web tracks",
                ],
                "course_slug": "python-for-beginners-uzbekistan",
                "center_slug": "web-development",
            },
            {
                "id": "backend",
                "label": "Moving into backend",
                "headline": "Professional backend growth through Django, auth, dashboards, and architecture",
                "description": "If you already know the basics but want to see how real systems come together, this is the fastest value path.",
                "bullets": [
                    "See a production-style SaaS architecture end to end",
                    "Understand how API, database, and access control work together",
                    "Build a stronger signal for interviews and freelance work",
                ],
                "course_slug": "django-fullstack-mastery",
                "center_slug": "backend-engineering",
            },
            {
                "id": "api",
                "label": "Becoming an API specialist",
                "headline": "Write reliable endpoints for frontend, mobile, and third-party integrations",
                "description": "If you want to strengthen the API layer inside product backend work, this route gets practical fast.",
                "bullets": [
                    "Level up DRF patterns and resource modeling",
                    "Work with permissions, docs, and predictable error flows",
                    "Learn to write collaboration-friendly API contracts",
                ],
                "course_slug": "rest-api-with-drf",
                "center_slug": "backend-engineering",
            },
        ],
        "blog_spotlight_label": "Editor pick",
    },
    "ru": {
        "trust_strip": [
            "Реальные SaaS-кейсы",
            "Еженедельный разбор с ментором",
            "Обучение с упором на портфолио",
            "SEO и product thinking",
            "Узбекская и английская tech-терминология",
        ],
        "momentum_label": "Динамика платформы",
        "momentum_title": "Студенты не просто смотрят уроки — они каждую неделю получают заметный результат",
        "momentum_description": "После онбординга каждый студент движется по понятным спринтам, получает точки обратной связи и deliverable, который можно показать публично.",
        "recent_activity": [
            {
                "name": "Dilshod Qodirov",
                "role": "Junior backend-разработчик",
                "action": "Завершил модуль REST API, реализовал token auth и throttling и обновил GitHub-портфолио.",
                "time": "12 мин назад",
                "metric": "2 коммита + 1 review",
            },
            {
                "name": "Madina Karimova",
                "role": "Студентка Computer Science",
                "action": "Завершила трек Python fundamentals и задеплоила свой mini-project expense tracker.",
                "time": "47 мин назад",
                "metric": "1 live-проект",
            },
            {
                "name": "Azizbek Juraev",
                "role": "Фриланс-разработчик",
                "action": "Завершил billing-ready dashboard flow внутри Django Fullstack Mastery.",
                "time": "1 час назад",
                "metric": "4.9 mentor score",
            },
            {
                "name": "Elena Sokolova",
                "role": "Продуктовый аналитик",
                "action": "Опубликовала первый analytics case study на основе data reporting workflow.",
                "time": "Сегодня",
                "metric": "3 insight-карточки",
            },
        ],
        "platform_pillars": [
            {
                "stat": "7 дней",
                "title": "Быстрый онбординг",
                "description": "Уже в первую неделю вы получаете подходящий маршрут обучения, рекомендованные курсы и практические задачи.",
            },
            {
                "stat": "2-3 проекта",
                "title": "Еженедельный спринт-ритм",
                "description": "Теория сразу закрепляется через мини-проект, рефакторинг или API-задачу.",
            },
            {
                "stat": "24 часа",
                "title": "Окно обратной связи",
                "description": "По заданиям и вопросам вы получаете короткий, практичный и product-minded ответ.",
            },
        ],
        "journey_label": "Цикл роста",
        "journey_title": "Платформа спроектирована не для пассивного просмотра, а для роста",
        "journey_description": "Каждый этап заканчивается решением реальной задачи, видимым результатом и понятным следующим шагом.",
        "journey_steps": [
            {"step": "01", "title": "Диагностический старт", "description": "Ваш уровень, цели и темп определяют правильную стартовую точку."},
            {"step": "02", "title": "Практический спринт", "description": "Каждый модуль превращается в landing page, API, dashboard, задачу по базе данных или deploy-шаг."},
            {"step": "03", "title": "Цикл ревью", "description": "Code quality, naming, UX и architecture усиливаются через короткую обратную связь."},
            {"step": "04", "title": "Результат на запуске", "description": "На выходе — GitHub-ready работа, portfolio case study или talking points для интервью."},
        ],
        "experience_label": "Формат обучения",
        "experience_title": "Мы объединили курс, менторскую поддержку и карьерный сигнал в одном потоке",
        "experience_description": "Вместе эти режимы делают EduPlanet не обычным LMS, а системой роста.",
        "experience_modes": [
            {
                "id": "sprint",
                "label": "Практические спринты",
                "metric": "2-3 практических build-а в неделю",
                "headline": "Теория сразу превращается в delivery flow, который можно пройти руками",
                "description": "В каждом курсе есть реальные product tasks: auth flow, API endpoint, responsive section, analytics query или deploy checklist.",
                "bullets": [
                    "Задачи, которые дают результат сразу после урока",
                    "Portfolio-deliverables, которые накапливаются со временем",
                    "Product thinking и clean execution растут вместе",
                ],
            },
            {
                "id": "review",
                "label": "Цикл code review",
                "metric": "Обратная связь по naming, UX и architecture",
                "headline": "Вы строите не просто рабочие, а профессиональные и readable решения",
                "description": "Упрощенный review layer быстро подсвечивает слабые места в коде, copy или layout-решениях.",
                "bullets": [
                    "Более сильная привычка к cleanup и refactoring",
                    "Readable API и maintainable templates",
                    "Мост от junior output к product-minded engineering",
                ],
            },
            {
                "id": "career",
                "label": "Карьерный апгрейд",
                "metric": "Roadmap, портфолио и уверенность",
                "headline": "Каждый трек заканчивается сигналом, который доказывает готовность к следующему шагу",
                "description": "Помимо completion вы получаете GitHub positioning, направление для case study, talking points для интервью и понятный next-step plan.",
                "bullets": [
                    "Практическая помощь с portfolio positioning",
                    "Proof-of-work для freelance или hiring-разговоров",
                    "Ясный порядок следующих навыков",
                ],
            },
        ],
        "path_label": "Навигатор пути",
        "path_title": "Какой маршрут даст вам максимальный импульс прямо сейчас?",
        "path_description": "Выберите цель, которая ближе всего вам, и платформа покажет лучший курс и направление.",
        "path_primary": "Рекомендованный курс",
        "path_secondary": "О направлении",
        "goal_paths": [
            {
                "id": "starter",
                "label": "Старт с нуля",
                "headline": "Сначала соберите уверенность через Python fundamentals и web-контекст",
                "description": "Если вы только входите в программирование, первая победа — не только синтаксис, а уверенность продолжать путь.",
                "bullets": [
                    "Начнете использовать Python-синтаксис без страха",
                    "Откроете GitHub-портфолио первыми мини-проектами",
                    "Естественно перейдете в Django или web-треки",
                ],
                "course_slug": "python-for-beginners-uzbekistan",
                "center_slug": "web-development",
            },
            {
                "id": "backend",
                "label": "Переход в backend",
                "headline": "Профессиональный рост в backend через Django, auth, dashboards и architecture",
                "description": "Если база у вас уже есть, но хочется глубже понять реальные системы, это самый быстрый value-path.",
                "bullets": [
                    "Увидите production-style SaaS architecture end to end",
                    "Поймете, как вместе работают API, database и access control",
                    "Усилите сигнал для интервью и freelance-задач",
                ],
                "course_slug": "django-fullstack-mastery",
                "center_slug": "backend-engineering",
            },
            {
                "id": "api",
                "label": "Стать API-специалистом",
                "headline": "Писать надежные endpoint'ы для frontend, mobile и third-party integrations",
                "description": "Если хотите укрепить именно API-слой в product-backend, этот маршрут быстро дает практику.",
                "bullets": [
                    "Укрепите DRF patterns и resource modeling",
                    "Поработаете с permissions, docs и predictable errors",
                    "Научитесь писать team-friendly API contracts",
                ],
                "course_slug": "rest-api-with-drf",
                "center_slug": "backend-engineering",
            },
        ],
        "blog_spotlight_label": "Выбор редакции",
    },
}

UNSPLASH = {
    "python": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=1200&q=80",
    "laptop": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80",
    "backend": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=1200&q=80",
    "data": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
    "devops": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
    "team": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1200&q=80",
    "learning": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80",
    "workspace": "https://images.unsplash.com/photo-1496171367470-9ed9a91ea931?auto=format&fit=crop&w=1200&q=80",
    "notebook": "https://images.unsplash.com/photo-1513258496099-48168024aec0?auto=format&fit=crop&w=1200&q=80",
    "server": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80",
    "mentor": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=1200&q=80",
}

CATEGORY_DATA = [
    {
        "slug": "web-development",
        "name": "Web Development",
        "description": "Frontend fundamentals, browser workflows va fullstack project assembly bo'yicha amaliy yo'nalish.",
        "icon": "</>",
        "translations": {
            "name": {"uz": "Web Development", "en": "Web Development", "ru": "Веб-разработка"},
            "description": {
                "uz": "Frontend fundamentals, browser workflows va fullstack project assembly bo'yicha amaliy yo'nalish.",
                "en": "A practical track focused on frontend fundamentals, browser workflows, and fullstack project assembly.",
                "ru": "Практическое направление по frontend fundamentals, browser workflow и сборке fullstack-проектов.",
            },
        },
    },
    {
        "slug": "backend-engineering",
        "name": "Backend Engineering",
        "description": "API design, authentication, database architecture va scalable Django systems uchun chuqur yo'nalish.",
        "icon": "{ }",
        "translations": {
            "name": {"uz": "Backend Engineering", "en": "Backend Engineering", "ru": "Бэкенд-инженерия"},
            "description": {
                "uz": "API design, authentication, database architecture va scalable Django systems uchun chuqur yo'nalish.",
                "en": "An in-depth path for API design, authentication, database architecture, and scalable Django systems.",
                "ru": "Глубокий трек по API design, authentication, database architecture и scalable Django systems.",
            },
        },
    },
    {
        "slug": "data-science",
        "name": "Data Science",
        "description": "Python, analytics va data storytelling orqali biznes qarorlarini tushunishga yordam beradigan yo'nalish.",
        "icon": "AI",
        "translations": {
            "name": {"uz": "Data Science", "en": "Data Science", "ru": "Наука о данных"},
            "description": {
                "uz": "Python, analytics va data storytelling orqali biznes qarorlarini tushunishga yordam beradigan yo'nalish.",
                "en": "A data-focused track that uses Python, analytics, and data storytelling to support business decisions.",
                "ru": "Направление по Python, analytics и data storytelling для бизнес-решений.",
            },
        },
    },
    {
        "slug": "devops",
        "name": "DevOps",
        "description": "Deployment, monitoring, Docker va CI/CD jarayonlarini Python product workflow bilan bog'laydigan markaz.",
        "icon": "CI",
        "translations": {
            "name": {"uz": "DevOps", "en": "DevOps", "ru": "DevOps"},
            "description": {
                "uz": "Deployment, monitoring, Docker va CI/CD jarayonlarini Python product workflow bilan bog'laydigan markaz.",
                "en": "A practical center connecting deployment, monitoring, Docker, and CI/CD with Python product workflows.",
                "ru": "Практический центр, который связывает deployment, monitoring, Docker и CI/CD с Python product workflows.",
            },
        },
    },
]

CENTER_DATA = [
    {
        "slug": "web-development",
        "name": "Web Development",
        "headline": "Brauzerdan production releasegacha bo'lgan yo'lni real loyihalar bilan o'rganing",
        "description": "Web Development markazi HTML, CSS, JavaScript fundamentals va Django templatingni bitta tizimli yo'lga birlashtiradi. Talabalar landing page, dashboard, reusable component system va conversion-focused UI yozishni o'rganadi. Fokus faqat kodda emas: product thinking, UX, SEO va performance ham har bir modulga singdirilgan. Bu markazda siz portfolio uchun foydali, ko'rinishdan tortib deploygacha tugallangan loyihalar qilasiz.",
        "location": "Tashkent, Mirzo Ulugbek district",
        "email": "web@eduplanet.uz",
        "phone_number": "+998901112233",
        "image": UNSPLASH["learning"],
        "website": "https://eduplanet.uz/web-development",
        "students_count": 420,
        "mentors_count": 6,
        "courses_count": 2,
        "features": [
            "Responsive UI, Tailwind va conversion-focused layoutlar",
            "Portfolio-ready landing page va SaaS dashboard loyihalari",
            "SEO basics, semantic HTML va performance workflow",
        ],
        "categories": ["web-development"],
        "translations": {
            "headline": {
                "uz": "Brauzerdan production releasegacha bo'lgan yo'lni real loyihalar bilan o'rganing",
                "en": "Learn the full path from browser basics to production release through real projects",
                "ru": "Изучайте путь от основ работы в браузере до production release через реальные проекты",
            },
            "description": {
                "uz": "Web Development markazi HTML, CSS, JavaScript fundamentals va Django templatingni bitta tizimli yo'lga birlashtiradi. Talabalar landing page, dashboard, reusable component system va conversion-focused UI yozishni o'rganadi. Fokus faqat kodda emas: product thinking, UX, SEO va performance ham har bir modulga singdirilgan. Bu markazda siz portfolio uchun foydali, ko'rinishdan tortib deploygacha tugallangan loyihalar qilasiz.",
                "en": "The Web Development center combines HTML, CSS, JavaScript fundamentals, and Django templating into one structured path. Students learn to build landing pages, dashboards, reusable component systems, and conversion-focused UI. The focus goes beyond code: product thinking, UX, SEO, and performance are embedded in every module. You leave with polished, portfolio-ready projects from design to deployment.",
                "ru": "Центр веб-разработки объединяет HTML, CSS, JavaScript fundamentals и Django templating в один системный путь. Студенты учатся создавать landing page, dashboard, reusable component systems и conversion-focused UI. Фокус не только на коде: product thinking, UX, SEO и performance встроены в каждый модуль. На выходе — законченные portfolio-ready проекты от дизайна до deployment.",
            },
        },
    },
    {
        "slug": "backend-engineering",
        "name": "Backend Engineering",
        "headline": "Scalable API, database architecture va product logic yozishni chuqur o'rganing",
        "description": "Backend Engineering markazi Python ecosystem ichida eng talabgir ko'nikmalarni yig'adi: Django architecture, REST API, authentication, PostgreSQL va clean code. Har bir kurs product constraints bilan yozilgan - ya'ni demo emas, real startup backlogga o'xshash tasklar mavjud. Siz service layer, background task, schema design, testing va documentation bilan ishlaysiz. Natijada nafaqat kod yozasiz, balki tizimni tushunadigan muhandis sifatida o'sasiz.",
        "location": "Tashkent, Yunusobod district",
        "email": "backend@eduplanet.uz",
        "phone_number": "+998901112244",
        "image": UNSPLASH["backend"],
        "website": "https://eduplanet.uz/backend-engineering",
        "students_count": 510,
        "mentors_count": 7,
        "courses_count": 4,
        "features": [
            "REST API, authentication, permissions va payment-ready architecture",
            "PostgreSQL schema design, optimization va debugging",
            "Clean code, testing, documentation va team workflow",
        ],
        "categories": ["backend-engineering"],
        "translations": {
            "headline": {
                "uz": "Scalable API, database architecture va product logic yozishni chuqur o'rganing",
                "en": "Go deep on scalable APIs, database architecture, and product logic",
                "ru": "Глубоко изучите scalable API, database architecture и product logic",
            },
            "description": {
                "uz": "Backend Engineering markazi Python ecosystem ichida eng talabgir ko'nikmalarni yig'adi: Django architecture, REST API, authentication, PostgreSQL va clean code. Har bir kurs product constraints bilan yozilgan - ya'ni demo emas, real startup backlogga o'xshash tasklar mavjud. Siz service layer, background task, schema design, testing va documentation bilan ishlaysiz. Natijada nafaqat kod yozasiz, balki tizimni tushunadigan muhandis sifatida o'sasiz.",
                "en": "The Backend Engineering center bundles the most valuable skills inside the Python ecosystem: Django architecture, REST API design, authentication, PostgreSQL, and clean code. Every course is shaped around product constraints rather than toy tasks. You work through service layers, background jobs, schema design, testing, and documentation, so you grow into an engineer who understands systems, not just syntax.",
                "ru": "Центр backend-инженерии собирает самые востребованные навыки внутри Python ecosystem: Django architecture, REST API design, authentication, PostgreSQL и clean code. Каждый курс построен не на toy tasks, а на product constraints. Вы проходите service layers, background jobs, schema design, testing и documentation, чтобы стать инженером, который понимает системы, а не только синтаксис.",
            },
        },
    },
    {
        "slug": "data-science",
        "name": "Data Science",
        "headline": "Python bilan data thinking, analytics va insight-driven qaror qabul qilishni o'rganing",
        "description": "Data Science markazi Pythonni faqat kod yozish vositasi sifatida emas, balki tahlil va qaror qabul qilish platformasi sifatida ko'rsatadi. Bu yerda siz pandas, SQL mindset, exploratory analysis va storytellingni amaliy datasetlar ustida mashq qilasiz. Kurslar product manager, analyst yoki backend developer bo'lishidan qat'i nazar, data bilan ishlashga ishonch beradi. Ayniqsa, dashboardlar va reporting tizimlari quradigan mutaxassislar uchun bu markaz kuchli poydevor beradi.",
        "location": "Tashkent, Shaykhantohur district",
        "email": "data@eduplanet.uz",
        "phone_number": "+998901112255",
        "image": UNSPLASH["data"],
        "website": "https://eduplanet.uz/data-science",
        "students_count": 180,
        "mentors_count": 4,
        "courses_count": 1,
        "features": [
            "Python, pandas va notebook workflow",
            "Business metrics, EDA va reporting skilllari",
            "Data-driven portfolio case studylar",
        ],
        "categories": ["data-science"],
        "translations": {
            "headline": {
                "uz": "Python bilan data thinking, analytics va insight-driven qaror qabul qilishni o'rganing",
                "en": "Use Python to build data thinking, analytics habits, and insight-driven decision making",
                "ru": "Изучите Python для data thinking, analytics и insight-driven решений",
            },
            "description": {
                "uz": "Data Science markazi Pythonni faqat kod yozish vositasi sifatida emas, balki tahlil va qaror qabul qilish platformasi sifatida ko'rsatadi. Bu yerda siz pandas, SQL mindset, exploratory analysis va storytellingni amaliy datasetlar ustida mashq qilasiz. Kurslar product manager, analyst yoki backend developer bo'lishidan qat'i nazar, data bilan ishlashga ishonch beradi. Ayniqsa, dashboardlar va reporting tizimlari quradigan mutaxassislar uchun bu markaz kuchli poydevor beradi.",
                "en": "The Data Science center treats Python not only as a programming language but as a platform for analysis and decision-making. You practice pandas, SQL thinking, exploratory analysis, and storytelling on practical datasets. Whether you aim to be a product manager, analyst, or backend engineer, this center helps you become more confident with data and reporting workflows.",
                "ru": "Центр Data Science показывает Python не только как язык программирования, но и как платформу для анализа и принятия решений. Вы практикуете pandas, SQL mindset, exploratory analysis и storytelling на реальных датасетах. Неважно, хотите ли вы стать product manager, analyst или backend engineer — этот центр помогает уверенно работать с данными и отчетностью.",
            },
        },
    },
    {
        "slug": "devops",
        "name": "DevOps",
        "headline": "Django ilovalarni deploy, monitor va scale qilish uchun zarur asoslarni egallang",
        "description": "DevOps markazi product jamoasida tez-tez kechikadigan, lekin eng muhim qatlamlardan birini yoritadi: deployment va operational confidence. Siz Docker, CI/CD, environment management, logs, monitoring va release hygiene bilan ishlaysiz. Kurslar aynan Python va Django loyihalari kontekstida yozilgan, shuning uchun o'rganilgan bilimlarni birinchi haftadanoq amalda qo'llash mumkin. Backend developer uchun bu yo'nalish ishga tayyorlikni sezilarli oshiradi.",
        "location": "Tashkent, Yakkasaroy district",
        "email": "devops@eduplanet.uz",
        "phone_number": "+998901112266",
        "image": UNSPLASH["devops"],
        "website": "https://eduplanet.uz/devops",
        "students_count": 140,
        "mentors_count": 3,
        "courses_count": 1,
        "features": [
            "Docker, GitHub Actions va release checklist",
            "Cloud deployment, monitoring va logs bilan ishlash",
            "Python teams uchun CI/CD best practices",
        ],
        "categories": ["devops"],
        "translations": {
            "headline": {
                "uz": "Django ilovalarni deploy, monitor va scale qilish uchun zarur asoslarni egallang",
                "en": "Master the essentials for deploying, monitoring, and scaling Django applications",
                "ru": "Освойте основы deployment, monitoring и масштабирования Django-приложений",
            },
            "description": {
                "uz": "DevOps markazi product jamoasida tez-tez kechikadigan, lekin eng muhim qatlamlardan birini yoritadi: deployment va operational confidence. Siz Docker, CI/CD, environment management, logs, monitoring va release hygiene bilan ishlaysiz. Kurslar aynan Python va Django loyihalari kontekstida yozilgan, shuning uchun o'rganilgan bilimlarni birinchi haftadanoq amalda qo'llash mumkin. Backend developer uchun bu yo'nalish ishga tayyorlikni sezilarli oshiradi.",
                "en": "The DevOps center covers one of the most important yet often delayed layers in product teams: deployment and operational confidence. You work with Docker, CI/CD, environment management, logs, monitoring, and release hygiene. Because every module is written in the context of Python and Django projects, you can apply the lessons quickly to real work.",
                "ru": "Центр DevOps закрывает один из самых важных, но часто откладываемых слоев в product-командах: deployment и operational confidence. Вы работаете с Docker, CI/CD, environment management, logs, monitoring и release hygiene. Каждый модуль написан в контексте Python- и Django-проектов, поэтому знания можно быстро перенести в реальную работу.",
            },
        },
    },
]

COURSE_DATA = [
    {
        "slug": "python-for-beginners-uzbekistan",
        "center": "web-development",
        "name": "Python for Beginners: Noldan Real Loyihalargacha",
        "subtitle": "Python course Uzbekistan bozoriga mos ravishda tuzilgan, boshlovchilar uchun eng qulay start",
        "description": "Bu kurs dasturlashni endi boshlayotganlar uchun qurilgan, lekin sifati bo'yicha junior developer workflowga juda yaqin. Birinchi modullarda siz Python sintaksisi, data types, conditions, loops va functionsni o'rganasiz. Keyingi bosqichlarda fayllar bilan ishlash, API'dan ma'lumot olish, oddiy automation skriptlari yozish va mini projectlar qilish orqali amaliy ishonch hosil qilasiz. Har bir dars Uzbek tilida sodda tushuntiriladi, lekin real engineering terminology ham to'g'ri ishlatiladi. Kurs yakunida siz faqat theory bilgan talaba emas, balki GitHub'ga qo'ysa bo'ladigan 3 ta amaliy ishga ega bo'lasiz.",
        "level": "Beginner",
        "duration": "18h 40m",
        "lessons_count": 42,
        "students_count": 1280,
        "hours_watched": 2400,
        "price": 690000,
        "rating": Decimal("4.9"),
        "image": UNSPLASH["python"],
        "featured": True,
        "highlights": [
            "Python fundamentals va first automation scripts",
            "GitHub workflow va portfolio-ready mini projectlar",
            "Amaliy homework va mentor feedback",
        ],
        "outcomes": [
            "Python syntax va standard library bilan erkin ishlaysiz",
            "CLI utility, parser va oddiy API integration yozasiz",
            "Backend learning pathga o'tish uchun mustahkam poydevorga ega bo'lasiz",
        ],
        "curriculum": [
            "Python syntax, operators va control flow",
            "Functions, modules va code organization",
            "Files, JSON, requests va automation",
            "Mini projects: expense tracker, telegram parser, API consumer",
        ],
        "translations": {
            "name": {"uz": "Python for Beginners: Noldan Real Loyihalargacha", "en": "Python for Beginners: From Zero to Real Projects", "ru": "Python для начинающих: от нуля до реальных проектов"},
            "subtitle": {
                "uz": "Python course Uzbekistan bozoriga mos ravishda tuzilgan, boshlovchilar uchun eng qulay start",
                "en": "A structured starting point for beginners built around the Uzbekistan Python learning market",
                "ru": "Удобный старт для новичков, собранный с учетом запроса Python course Uzbekistan",
            },
            "description": {
                "uz": "Bu kurs dasturlashni endi boshlayotganlar uchun qurilgan, lekin sifati bo'yicha junior developer workflowga juda yaqin. Birinchi modullarda siz Python sintaksisi, data types, conditions, loops va functionsni o'rganasiz. Keyingi bosqichlarda fayllar bilan ishlash, API'dan ma'lumot olish, oddiy automation skriptlari yozish va mini projectlar qilish orqali amaliy ishonch hosil qilasiz. Har bir dars Uzbek tilida sodda tushuntiriladi, lekin real engineering terminology ham to'g'ri ishlatiladi. Kurs yakunida siz faqat theory bilgan talaba emas, balki GitHub'ga qo'ysa bo'ladigan 3 ta amaliy ishga ega bo'lasiz.",
                "en": "This course is designed for complete beginners but taught close to a junior developer workflow. You start with Python syntax, data types, conditions, loops, and functions, then move into files, APIs, automation scripts, and practical mini-projects. The lessons stay beginner-friendly while using real engineering terminology. By the end, you leave not only with theory but with three portfolio pieces you can publish on GitHub.",
                "ru": "Этот курс создан для тех, кто только начинает, но по подходу близок к junior developer workflow. Сначала вы разбираете Python syntax, data types, conditions, loops и functions, затем переходите к работе с файлами, API, automation scripts и практическим мини-проектам. Объяснение простое, но терминология реальная. На выходе у вас будет не только теория, но и три GitHub-ready работы.",
            },
        },
        "seo_title": "Python course Uzbekistan | Python for Beginners by Asilbek Mirolimov",
        "seo_description": "Start your programming journey today with a beginner-friendly Python course from Tashkent mentor Asilbek Mirolimov.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["Python for Beginners", "Python darslari", "Dasturlashni o'rganish"]),
        "videos": [
            ("Python Setup va Birinchi Script", "Muhitni to'g'ri sozlash, editor tanlash va birinchi Python faylni ishga tushirish.", "https://www.youtube.com/watch?v=rfscVS0vtbw", UNSPLASH["workspace"], "22m", True),
            ("Data Types va Input/Output", "String, integer, list va foydalanuvchi inputi bilan ishlashni real misollarda ko'ramiz.", "https://www.youtube.com/watch?v=OH86oLzVzzw", UNSPLASH["notebook"], "28m", False),
            ("Functions bilan Kodni Tartiblash", "Reusable code yozish va kichik utility funksiyalar tuzishni mashq qilamiz.", "https://www.youtube.com/watch?v=9Os0o3wzS_I", UNSPLASH["mentor"], "31m", False),
        ],
    },
    {
        "slug": "web-development-bootcamp-django",
        "center": "web-development",
        "name": "Web Development Bootcamp: HTML, CSS, JavaScript va Django",
        "subtitle": "Frontenddan backendgacha bo'lgan fullstack yo'lni bitta bootcamp formatida o'rganing",
        "description": "Agar siz bitta yo'nalishda to'xtab qolmasdan, butun web product qanday yig'ilishini tushunmoqchi bo'lsangiz, bu bootcamp aynan siz uchun. Kursda semantic HTML, responsive CSS, JavaScript fundamentals va Django templatelari yagona loyiha ustida qo'llanadi. Siz marketing landing page, student dashboard, blog page va course catalog yaratib, UI va backendni birlashtirasiz. Shuningdek, conversion copy, forms UX, accessibility va SEO basics ham alohida modul sifatida beriladi. Bu kurs ko'p qirrali mutaxassis bo'lishni istaganlar uchun kuchli start nuqtasi.",
        "level": "Beginner",
        "duration": "24h 10m",
        "lessons_count": 56,
        "students_count": 910,
        "hours_watched": 1880,
        "price": 890000,
        "rating": Decimal("4.8"),
        "image": UNSPLASH["laptop"],
        "featured": True,
        "highlights": [
            "Landing page, dashboard va blog layoutlar",
            "JavaScript interactions va form UX",
            "Django template rendering va deployment overview",
        ],
        "outcomes": [
            "Fullstack productning qanday yig'ilishini tushunasiz",
            "Tailwindga tayyor semantic markup yozasiz",
            "Portfolio uchun real SaaS landing page yaratib chiqasiz",
        ],
        "curriculum": [
            "Semantic HTML va responsive CSS systems",
            "JavaScript DOM, forms va reusable interactions",
            "Django templates, views va routing",
            "SEO, accessibility va deploy checklist",
        ],
        "translations": {
            "name": {"uz": "Web Development Bootcamp: HTML, CSS, JavaScript va Django", "en": "Web Development Bootcamp: HTML, CSS, JavaScript and Django", "ru": "Web Development Bootcamp: HTML, CSS, JavaScript и Django"},
            "subtitle": {
                "uz": "Frontenddan backendgacha bo'lgan fullstack yo'lni bitta bootcamp formatida o'rganing",
                "en": "Learn the fullstack path from frontend to backend inside one practical bootcamp",
                "ru": "Изучите полный fullstack-путь от frontend до backend в одном практическом bootcamp",
            },
            "description": {
                "uz": "Agar siz bitta yo'nalishda to'xtab qolmasdan, butun web product qanday yig'ilishini tushunmoqchi bo'lsangiz, bu bootcamp aynan siz uchun. Kursda semantic HTML, responsive CSS, JavaScript fundamentals va Django templatelari yagona loyiha ustida qo'llanadi. Siz marketing landing page, student dashboard, blog page va course catalog yaratib, UI va backendni birlashtirasiz. Shuningdek, conversion copy, forms UX, accessibility va SEO basics ham alohida modul sifatida beriladi. Bu kurs ko'p qirrali mutaxassis bo'lishni istaganlar uchun kuchli start nuqtasi.",
                "en": "If you want to understand how an entire web product comes together instead of staying in one narrow lane, this bootcamp is for you. It combines semantic HTML, responsive CSS, JavaScript fundamentals, and Django templates inside one integrated project. You build a marketing landing page, student dashboard, blog page, and course catalog while learning UX, accessibility, SEO, and conversion copy.",
                "ru": "Если вы хотите понять, как собирается весь web-product, а не оставаться в одном узком направлении, этот bootcamp для вас. В нем semantic HTML, responsive CSS, JavaScript fundamentals и Django templates собраны в один общий проект. Вы создаете landing page, student dashboard, blog page и course catalog, одновременно прокачивая UX, accessibility, SEO и conversion copy.",
            },
        },
        "seo_title": "Web Development Bootcamp | Django course online by Asilbek Mirolimov",
        "seo_description": "Become a job-ready developer by learning HTML, CSS, JavaScript and Django in one practical bootcamp.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["web development bootcamp", "frontend va backend kursi", "Django bootcamp"]),
        "videos": [
            ("Semantic HTML va Layout Thinking", "Sections, hierarchy va content-first layout yozishni o'rganamiz.", "https://www.youtube.com/watch?v=qz0aGYrrlhU", UNSPLASH["learning"], "26m", True),
            ("Responsive CSS Strategy", "Breakpoints, spacing system va reusable componentlar quriladi.", "https://www.youtube.com/watch?v=1PnVor36_40", UNSPLASH["laptop"], "34m", False),
            ("Django Templates in Action", "Dynamic course cards va content blocks render qilishni ko'ramiz.", "https://www.youtube.com/watch?v=F5mRW0jo-U4", UNSPLASH["workspace"], "29m", False),
        ],
    },
    {
        "slug": "django-fullstack-mastery",
        "center": "backend-engineering",
        "name": "Django Fullstack Mastery: SaaS Ilovalarni Qurish",
        "subtitle": "Django course online formatida auth, payments, dashboards va subscription flow bilan to'liq product qurish",
        "description": "Django Fullstack Mastery kursi backendni yaxshi ko'radigan, lekin productni end-to-end ko'ra oladigan mutaxassis bo'lishni xohlaydiganlar uchun yozilgan. Siz users, permissions, billing-ready architecture, dashboards, email workflow, blog va course management kabi modullarni bosqichma-bosqich qurasiz. Kurs ichida faqat CRUD emas, balki feature prioritization, naming, modularity va launch readinessga ham katta urg'u beriladi. Natijada siz real SaaS product skeletonini noldan ko'tara oladigan darajaga kelasiz. Interview va freelance bozorda aynan shu kompetensiya sizni ajratib turadi.",
        "level": "Intermediate",
        "duration": "27h 35m",
        "lessons_count": 61,
        "students_count": 760,
        "hours_watched": 1650,
        "price": 1190000,
        "rating": Decimal("4.9"),
        "image": UNSPLASH["backend"],
        "featured": True,
        "highlights": [
            "Auth, role-based permissions va payments-ready structure",
            "Reusable apps, clean routing va template composition",
            "Launch checklist, analytics va onboarding flow",
        ],
        "outcomes": [
            "Django bilan productionga yaqin SaaS product qurasiz",
            "Monolith architecture ichida scalable folder structure yozasiz",
            "Feature delivery, UX va backendni bitta product sifatida ko'rasiz",
        ],
        "curriculum": [
            "Project architecture va reusable apps",
            "Authentication, profile, subscription va access control",
            "Course, blog va dashboard modules",
            "Deployment readiness, analytics va growth hooks",
        ],
        "translations": {
            "name": {"uz": "Django Fullstack Mastery: SaaS Ilovalarni Qurish", "en": "Django Fullstack Mastery: Build SaaS Applications", "ru": "Django Fullstack Mastery: создание SaaS-приложений"},
            "subtitle": {
                "uz": "Django course online formatida auth, payments, dashboards va subscription flow bilan to'liq product qurish",
                "en": "Build a complete product with auth, payments, dashboards, and subscription flows in a practical Django course online",
                "ru": "Соберите полный продукт с auth, payments, dashboards и subscription flow в практическом Django course online",
            },
            "description": {
                "uz": "Django Fullstack Mastery kursi backendni yaxshi ko'radigan, lekin productni end-to-end ko'ra oladigan mutaxassis bo'lishni xohlaydiganlar uchun yozilgan. Siz users, permissions, billing-ready architecture, dashboards, email workflow, blog va course management kabi modullarni bosqichma-bosqich qurasiz. Kurs ichida faqat CRUD emas, balki feature prioritization, naming, modularity va launch readinessga ham katta urg'u beriladi. Natijada siz real SaaS product skeletonini noldan ko'tara oladigan darajaga kelasiz. Interview va freelance bozorda aynan shu kompetensiya sizni ajratib turadi.",
                "en": "Django Fullstack Mastery is written for engineers who love backend work but want to understand products end to end. You build users, permissions, billing-ready architecture, dashboards, email workflows, blogs, and course management step by step. The emphasis goes beyond CRUD into feature prioritization, naming, modularity, and launch readiness. By the end, you can create a real SaaS skeleton from scratch.",
                "ru": "Django Fullstack Mastery создан для тех, кто любит backend, но хочет видеть product end to end. Вы пошагово собираете users, permissions, billing-ready architecture, dashboards, email workflow, blog и course management. Акцент не только на CRUD, но и на feature prioritization, naming, modularity и launch readiness. В результате вы умеете поднять реальный SaaS skeleton с нуля.",
            },
        },
        "seo_title": "Django course online | Django Fullstack Mastery by Asilbek Mirolimov",
        "seo_description": "Learn from real-world experience and build a production-style Django SaaS product with authentication, dashboards and billing-ready flows.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["Django Fullstack Mastery", "Django SaaS course", "fullstack django"]),
        "videos": [
            ("Project Architecture Overview", "Apps, naming conventions va scalable folder structure tanlanadi.", "https://www.youtube.com/watch?v=F5mRW0jo-U4", UNSPLASH["backend"], "33m", True),
            ("Authentication va Access Control", "Role-based permissions va user lifecycle ustida ishlaymiz.", "https://www.youtube.com/watch?v=dAfg3leE0YQ", UNSPLASH["team"], "37m", False),
            ("SaaS Dashboard Composition", "Metrics cards, activity feed va CTA blocks integratsiya qilinadi.", "https://www.youtube.com/watch?v=PtQiiknWUcI", UNSPLASH["workspace"], "31m", False),
        ],
    },
    {
        "slug": "rest-api-with-drf",
        "center": "backend-engineering",
        "name": "REST API with Django REST Framework",
        "subtitle": "Mobile, frontend va third-party integrations uchun ishonchli API qatlamini yozing",
        "description": "REST API with DRF kursi frontend yoki mobile jamoa bilan ishlashni xohlaydigan backend developerlar uchun juda muhim. Siz serializer, viewset, permissions, throttling, filtering, versioning va documentationni real biznes scenario asosida o'rganasiz. Kurs davomida auth service, catalog API, order flow va analytics endpointlar kabi use-caselarga tayangan holda arxitektura quriladi. Shuningdek, performance, pagination va predictable error responses haqida ham amaliy qarorlar qabul qilasiz. Bu kurs sizni oddiy endpoint yozuvchidan product API engineer darajasiga olib chiqadi.",
        "level": "Intermediate",
        "duration": "16h 50m",
        "lessons_count": 38,
        "students_count": 640,
        "hours_watched": 1210,
        "price": 790000,
        "rating": Decimal("4.8"),
        "image": UNSPLASH["server"],
        "featured": False,
        "highlights": [
            "Serializers, viewsets va permissions deep dive",
            "Filtering, pagination, versioning va docs",
            "API reliability, errors va testing workflow",
        ],
        "outcomes": [
            "Frontend va mobile jamoalar bilan ishlashga tayyor API yozasiz",
            "DRF ichida clean patterns va reusable base classes qurasiz",
            "Swagger/Redocga mos documentation strategiyasini tushunasiz",
        ],
        "curriculum": [
            "API design principles va resource modeling",
            "Serializers, validation va nested objects",
            "Permissions, auth, throttling va filtering",
            "Testing, docs va deployment considerations",
        ],
        "translations": {
            "name": {"uz": "REST API with Django REST Framework", "en": "REST API with Django REST Framework", "ru": "REST API на Django REST Framework"},
            "subtitle": {
                "uz": "Mobile, frontend va third-party integrations uchun ishonchli API qatlamini yozing",
                "en": "Build a reliable API layer for mobile apps, frontend teams, and third-party integrations",
                "ru": "Пишите надежный API-слой для mobile, frontend и third-party integrations",
            },
            "description": {
                "uz": "REST API with DRF kursi frontend yoki mobile jamoa bilan ishlashni xohlaydigan backend developerlar uchun juda muhim. Siz serializer, viewset, permissions, throttling, filtering, versioning va documentationni real biznes scenario asosida o'rganasiz. Kurs davomida auth service, catalog API, order flow va analytics endpointlar kabi use-caselarga tayangan holda arxitektura quriladi. Shuningdek, performance, pagination va predictable error responses haqida ham amaliy qarorlar qabul qilasiz. Bu kurs sizni oddiy endpoint yozuvchidan product API engineer darajasiga olib chiqadi.",
                "en": "This course is essential for backend developers who want to collaborate with frontend or mobile teams. You learn serializers, viewsets, permissions, throttling, filtering, versioning, and documentation through real business scenarios. The architecture is built around use cases such as auth services, catalog APIs, order flows, and analytics endpoints, so the lessons stay practical and product-focused.",
                "ru": "Этот курс важен для backend-разработчиков, которые хотят эффективно работать с frontend- или mobile-командами. Вы изучаете serializers, viewsets, permissions, throttling, filtering, versioning и documentation на основе реальных бизнес-сценариев. Архитектура строится вокруг auth services, catalog API, order flow и analytics endpoints, поэтому все остается максимально практичным.",
            },
        },
        "seo_title": "REST API with DRF | Backend course Tashkent and online",
        "seo_description": "Master Django REST Framework and build production-style APIs for web, mobile and third-party integrations.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["REST API with DRF", "Django REST Framework course", "API design"]),
        "videos": [
            ("Serializer Design Principles", "Input validation va response shaping uchun to'g'ri strukturani tanlaymiz.", "https://www.youtube.com/watch?v=c708Nf0cHrs", UNSPLASH["server"], "24m", True),
            ("Permissions va Auth Patterns", "Session, token va role-based access control bilan ishlaymiz.", "https://www.youtube.com/watch?v=H0Z1b6A1lY0", UNSPLASH["team"], "27m", False),
            ("API Docs and Predictable Errors", "Consumer-friendly documentation va error contract yaratamiz.", "https://www.youtube.com/watch?v=Uyei2iDA4Hs", UNSPLASH["workspace"], "21m", False),
        ],
    },
    {
        "slug": "postgresql-for-developers",
        "center": "backend-engineering",
        "name": "PostgreSQL for Developers",
        "subtitle": "Database design, indexing va query optimization orqali backendni sezilarli kuchaytiring",
        "description": "Ko'p junior developerlar kodga ko'p vaqt ajratadi, lekin database qatlami haqida yetarlicha o'ylamaydi. Ushbu kurs aynan shu bo'shliqni yopadi. Siz relational modeling, joins, normalization, indexes, query plans va migration strategy kabi mavzularni Django kontekstida o'rganasiz. Real misollar sifatida e-commerce, analytics va LMS datasetlari ishlatiladi. Kursdan keyin siz API sekinligi yoki reporting xatolarining sababini database tomondan ko'ra olasiz.",
        "level": "Intermediate",
        "duration": "12h 20m",
        "lessons_count": 29,
        "students_count": 430,
        "hours_watched": 760,
        "price": 690000,
        "rating": Decimal("4.7"),
        "image": UNSPLASH["server"],
        "featured": False,
        "highlights": [
            "Schema design va query tuning",
            "Indexes, explain plans va reporting tables",
            "Django ORM bilan database-level thinking",
        ],
        "outcomes": [
            "Schema design qilishda product use-caselardan kelib chiqasiz",
            "Slow query va bad relationlarni aniqlay olasiz",
            "PostgreSQLni backend career uchun kuchli differentiatorga aylantirasiz",
        ],
        "curriculum": [
            "Relational modeling va normalization",
            "Indexes, joins va query plans",
            "Aggregations, reporting va materialized approaches",
            "Django ORM + PostgreSQL optimization workflow",
        ],
        "translations": {
            "name": {"uz": "PostgreSQL for Developers", "en": "PostgreSQL for Developers", "ru": "PostgreSQL для разработчиков"},
            "subtitle": {
                "uz": "Database design, indexing va query optimization orqali backendni sezilarli kuchaytiring",
                "en": "Strengthen your backend with better database design, indexing, and query optimization",
                "ru": "Усильте свой backend через database design, indexing и query optimization",
            },
            "description": {
                "uz": "Ko'p junior developerlar kodga ko'p vaqt ajratadi, lekin database qatlami haqida yetarlicha o'ylamaydi. Ushbu kurs aynan shu bo'shliqni yopadi. Siz relational modeling, joins, normalization, indexes, query plans va migration strategy kabi mavzularni Django kontekstida o'rganasiz. Real misollar sifatida e-commerce, analytics va LMS datasetlari ishlatiladi. Kursdan keyin siz API sekinligi yoki reporting xatolarining sababini database tomondan ko'ra olasiz.",
                "en": "Many junior developers spend time on code but not enough on the database layer. This course closes that gap. You study relational modeling, joins, normalization, indexes, query plans, and migration strategy through Django-flavored scenarios. Using e-commerce, analytics, and LMS datasets, you learn how to diagnose slow APIs and unreliable reporting from the database side.",
                "ru": "Многие junior-разработчики тратят много времени на код, но мало думают о слое базы данных. Этот курс закрывает этот пробел. Вы изучаете relational modeling, joins, normalization, indexes, query plans и migration strategy в Django-контексте. На примерах e-commerce, analytics и LMS вы учитесь понимать, почему медлит API или ломается отчетность.",
            },
        },
        "seo_title": "PostgreSQL for Developers | Backend database course by Asilbek Mirolimov",
        "seo_description": "Learn PostgreSQL design, indexing, query tuning and database architecture for modern Django products.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["PostgreSQL for Developers", "database course", "SQL optimization"]),
        "videos": [
            ("Schema Design for Product Teams", "Jadval va relationlarni use-case asosida loyihalaymiz.", "https://www.youtube.com/watch?v=qw--VYLpxG4", UNSPLASH["server"], "23m", True),
            ("Indexes va Query Plans", "EXPLAIN natijalarini o'qib, sekinlik sabablarini topamiz.", "https://www.youtube.com/watch?v=qoAL4MA3P04", UNSPLASH["workspace"], "26m", False),
            ("Django ORM Performance", "select_related, prefetch_related va aggregation strategiyalari.", "https://www.youtube.com/watch?v=F5mRW0jo-U4", UNSPLASH["mentor"], "18m", False),
        ],
    },
    {
        "slug": "clean-code-in-python",
        "center": "backend-engineering",
        "name": "Clean Code in Python: Maintainable Backend Architecture",
        "subtitle": "Kod sifati, naming va long-term maintainability orqali kuchli engineering odatlarini shakllantiring",
        "description": "Clean code mavzusi ko'pincha abstrakt ko'rinadi, ammo jamoa o'sgani sari aynan shu skill eng qimmat kompetensiyaga aylanadi. Bu kursda siz naming, module boundaries, function design, domain-driven thinking va refactoring taktikasini Python misollarida ko'rasiz. Legacy kodni qanday tushunish, commentni qachon yozish, qanday testlar barqaror bo'lishi va tech debtni qanday boshqarish haqida real qarorlar beriladi. Kurs code review madaniyatini ham yaxshilaydi. Yaxshi kod yozish - tezroq ishlashning eng ishonchli yo'li ekanini shu yerda his qilasiz.",
        "level": "Advanced",
        "duration": "10h 45m",
        "lessons_count": 24,
        "students_count": 360,
        "hours_watched": 620,
        "price": 590000,
        "rating": Decimal("4.8"),
        "image": UNSPLASH["mentor"],
        "featured": False,
        "highlights": [
            "Naming, boundaries va refactoring decisions",
            "Code review mindset va maintainability metrics",
            "Legacy code bilan ishlash strategiyasi",
        ],
        "outcomes": [
            "Kodni tezroq o'qiladigan va test-friendly qilasiz",
            "Refactor qilishda business riskni hisobga olasiz",
            "Jamoada senior signal beradigan engineering odatlar hosil bo'ladi",
        ],
        "curriculum": [
            "Readable Python patterns",
            "Naming, module boundaries va responsibilities",
            "Refactoring playbook va tech debt management",
            "Code review, tests va documentation discipline",
        ],
        "translations": {
            "name": {"uz": "Clean Code in Python: Maintainable Backend Architecture", "en": "Clean Code in Python: Maintainable Backend Architecture", "ru": "Clean Code in Python: поддерживаемая backend-архитектура"},
            "subtitle": {
                "uz": "Kod sifati, naming va long-term maintainability orqali kuchli engineering odatlarini shakllantiring",
                "en": "Build strong engineering habits through code quality, naming, and long-term maintainability",
                "ru": "Формируйте сильные engineering-привычки через code quality, naming и long-term maintainability",
            },
            "description": {
                "uz": "Clean code mavzusi ko'pincha abstrakt ko'rinadi, ammo jamoa o'sgani sari aynan shu skill eng qimmat kompetensiyaga aylanadi. Bu kursda siz naming, module boundaries, function design, domain-driven thinking va refactoring taktikasini Python misollarida ko'rasiz. Legacy kodni qanday tushunish, commentni qachon yozish, qanday testlar barqaror bo'lishi va tech debtni qanday boshqarish haqida real qarorlar beriladi. Kurs code review madaniyatini ham yaxshilaydi. Yaxshi kod yozish - tezroq ishlashning eng ishonchli yo'li ekanini shu yerda his qilasiz.",
                "en": "Clean code often sounds abstract until a team starts scaling. Then it becomes one of the most valuable engineering skills. In this course, you study naming, module boundaries, function design, domain-driven thinking, and refactoring tactics through practical Python examples. You learn how to approach legacy code, write durable tests, decide when comments help, and manage tech debt without blocking delivery.",
                "ru": "Тема clean code часто звучит абстрактно, но по мере роста команды становится одним из самых ценных engineering-навыков. В курсе вы разбираете naming, module boundaries, function design, domain-driven thinking и тактику refactoring на практических Python-примерах. Также учитесь работать с legacy, писать устойчивые tests и управлять tech debt без потери скорости доставки.",
            },
        },
        "seo_title": "Clean Code in Python | Advanced backend architecture course",
        "seo_description": "Learn clean code, refactoring, maintainable architecture and code review habits for real Python teams.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["clean code in python", "backend architecture", "refactoring"]),
        "videos": [
            ("Readable Functions and Naming", "Kichik, tushunarli va business-friendly funksiyalar yozishni ko'ramiz.", "https://www.youtube.com/watch?v=7EmboKQH8lM", UNSPLASH["mentor"], "19m", True),
            ("Module Boundaries", "Qaysi kod qaysi layerda yashashi kerakligini aniqlaymiz.", "https://www.youtube.com/watch?v=MF0jFKvS4SI", UNSPLASH["workspace"], "22m", False),
            ("Refactor Without Fear", "Testlar yordamida legacy kodni bosqichma-bosqich yaxshilaymiz.", "https://www.youtube.com/watch?v=2J9PqQ1G3mA", UNSPLASH["team"], "24m", False),
        ],
    },
    {
        "slug": "devops-basics-for-python-engineers",
        "center": "devops",
        "name": "DevOps Basics for Python Engineers",
        "subtitle": "Docker, CI/CD va deployment jarayonlarini backend engineer ko'zi bilan tushuning",
        "description": "Ko'p backend developerlar productionga chiqish jarayonida o'ziga ishonmaydi. Sababi - kod yaxshi bo'lsa ham, deploy va operational layer noaniq bo'lib qoladi. Ushbu kurs Docker image, environment variables, GitHub Actions, cloud deploy, logging va monitoring kabi mavzularni aynan Python loyiha misolida tushuntiradi. Siz release checklist yozish, rollback haqida o'ylash va xatolarni tez diagnostika qilish odatini shakllantirasiz. Bu skill junior darajadan mid-level'ga o'tishda juda katta ustunlik beradi.",
        "level": "Intermediate",
        "duration": "14h 05m",
        "lessons_count": 32,
        "students_count": 295,
        "hours_watched": 540,
        "price": 750000,
        "rating": Decimal("4.7"),
        "image": UNSPLASH["devops"],
        "featured": False,
        "highlights": [
            "Dockerfile, compose va secrets management",
            "CI/CD pipeline va release hygiene",
            "Logging, monitoring va rollback thinking",
        ],
        "outcomes": [
            "Python ilovani o'zingiz deploy qila olasiz",
            "CI/CD pipeline qurish asoslarini tushunasiz",
            "Operational muammolarni backend nuqtayi nazaridan tahlil qilasiz",
        ],
        "curriculum": [
            "Docker basics for Django apps",
            "Environment variables, build va secrets",
            "CI/CD with GitHub Actions",
            "Monitoring, logs va safe releases",
        ],
        "translations": {
            "name": {"uz": "DevOps Basics for Python Engineers", "en": "DevOps Basics for Python Engineers", "ru": "Основы DevOps для Python-инженеров"},
            "subtitle": {
                "uz": "Docker, CI/CD va deployment jarayonlarini backend engineer ko'zi bilan tushuning",
                "en": "Understand Docker, CI/CD, and deployment from the perspective of a backend engineer",
                "ru": "Поймите Docker, CI/CD и deployment глазами backend-инженера",
            },
            "description": {
                "uz": "Ko'p backend developerlar productionga chiqish jarayonida o'ziga ishonmaydi. Sababi - kod yaxshi bo'lsa ham, deploy va operational layer noaniq bo'lib qoladi. Ushbu kurs Docker image, environment variables, GitHub Actions, cloud deploy, logging va monitoring kabi mavzularni aynan Python loyiha misolida tushuntiradi. Siz release checklist yozish, rollback haqida o'ylash va xatolarni tez diagnostika qilish odatini shakllantirasiz. Bu skill junior darajadan mid-level'ga o'tishda juda katta ustunlik beradi.",
                "en": "Many backend developers feel uncertain when it comes time to ship to production. Even when the code is good, deployment and operations can feel vague. This course explains Docker images, environment variables, GitHub Actions, cloud deployment, logging, and monitoring through Python project examples. You learn to think in release checklists, rollback plans, and fast incident diagnosis.",
                "ru": "Многие backend-разработчики не чувствуют уверенности, когда дело доходит до production. Код может быть хорошим, но deploy и operations остаются неясными. Этот курс объясняет Docker images, environment variables, GitHub Actions, cloud deployment, logging и monitoring на примере Python-проектов. Вы учитесь мыслить release checklist'ами, rollback-планами и быстро диагностировать инциденты.",
            },
        },
        "seo_title": "DevOps Basics for Python Engineers | Deploy Django with confidence",
        "seo_description": "Learn Docker, CI/CD, deployment, logging and monitoring for real Python and Django applications.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["DevOps basics", "Docker for Django", "CI/CD Python"]),
        "videos": [
            ("Dockerizing a Django App", "Image, layers va environment configuration bilan ishlaymiz.", "https://www.youtube.com/watch?v=YFl2mCHdv24", UNSPLASH["devops"], "27m", True),
            ("CI/CD Fundamentals", "Pushdan deploygacha bo'lgan pipeline tasavvurini quramiz.", "https://www.youtube.com/watch?v=R8_veQiYBjI", UNSPLASH["server"], "25m", False),
            ("Monitoring and Incident Response", "Logs, alerts va rollback qarorlarini ko'rib chiqamiz.", "https://www.youtube.com/watch?v=0yWAtQ6wYNM", UNSPLASH["team"], "23m", False),
        ],
    },
    {
        "slug": "data-science-foundations-python",
        "center": "data-science",
        "name": "Data Science Foundations with Python",
        "subtitle": "Pandas, analysis mindset va dashboard-ready datasetlar bilan ishlashni o'rganing",
        "description": "Data Science Foundations kursi data sohasiga sakrash uchun emas, balki mustahkam poydevor qurish uchun yaratilgan. Siz pandas, cleaning, aggregation, visualization, notebook workflow va stakeholder-friendly xulosa chiqarishni amalda ko'rasiz. Kurs davomida student performance, sales va product analytics datasetlari bilan ishlanadi. Maqsad - data scientist bo'lishni xohlovchilarni ham, backend engineer sifatida analyticsni tushunmoqchi bo'lganlarni ham bitta platformada kuchaytirish. Bu skill bugungi product jamoalarda juda katta afzallik beradi.",
        "level": "Beginner",
        "duration": "15h 15m",
        "lessons_count": 34,
        "students_count": 255,
        "hours_watched": 500,
        "price": 720000,
        "rating": Decimal("4.8"),
        "image": UNSPLASH["data"],
        "featured": False,
        "highlights": [
            "Pandas, cleaning va notebook workflow",
            "Business metrics va storytelling",
            "Dashboard-ready dataset preparation",
        ],
        "outcomes": [
            "Datasetni tozalash va tahlil qilishga ishonch hosil qilasiz",
            "Vizualizatsiya orqali xulosa chiqarishni o'rganasiz",
            "Analytics project uchun boshlang'ich portfolio yaratasiz",
        ],
        "curriculum": [
            "Python for analysis and notebooks",
            "Pandas basics, cleaning va grouping",
            "Visual storytelling va metrics thinking",
            "Mini case studies for product and education data",
        ],
        "translations": {
            "name": {"uz": "Data Science Foundations with Python", "en": "Data Science Foundations with Python", "ru": "Основы Data Science с Python"},
            "subtitle": {
                "uz": "Pandas, analysis mindset va dashboard-ready datasetlar bilan ishlashni o'rganing",
                "en": "Learn pandas, analysis thinking, and how to work with dashboard-ready datasets",
                "ru": "Изучите pandas, analytical mindset и работу с dashboard-ready датасетами",
            },
            "description": {
                "uz": "Data Science Foundations kursi data sohasiga sakrash uchun emas, balki mustahkam poydevor qurish uchun yaratilgan. Siz pandas, cleaning, aggregation, visualization, notebook workflow va stakeholder-friendly xulosa chiqarishni amalda ko'rasiz. Kurs davomida student performance, sales va product analytics datasetlari bilan ishlanadi. Maqsad - data scientist bo'lishni xohlovchilarni ham, backend engineer sifatida analyticsni tushunmoqchi bo'lganlarni ham bitta platformada kuchaytirish. Bu skill bugungi product jamoalarda juda katta afzallik beradi.",
                "en": "This course is built not as a shortcut into data science, but as a strong foundation. You practice pandas, cleaning, aggregation, visualization, notebook workflow, and stakeholder-friendly communication on real datasets. Student performance, sales, and product analytics cases help you develop confidence whether you want to move into data work or simply become a more analytical backend engineer.",
                "ru": "Этот курс создан не как быстрый вход в data science, а как сильная база. Вы практикуете pandas, cleaning, aggregation, visualization, notebook workflow и понятное для stakeholders объяснение выводов на реальных датасетах. Кейсы по student performance, sales и product analytics помогают расти и будущим data-специалистам, и backend-инженерам.",
            },
        },
        "seo_title": "Data Science Foundations with Python | Practical analytics course",
        "seo_description": "Build data analysis confidence with pandas, business metrics and storytelling using practical Python datasets.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["data science foundations", "pandas course", "analytics with python"]),
        "videos": [
            ("Working with Notebooks", "Data analysis uchun notebook workflow va reproducibility haqida gaplashamiz.", "https://www.youtube.com/watch?v=5pf0_bpNbkw", UNSPLASH["data"], "20m", True),
            ("Pandas Grouping and Cleaning", "Real dataset ustida cleaning va aggregation strategiyasini mashq qilamiz.", "https://www.youtube.com/watch?v=vmEHCJofslg", UNSPLASH["notebook"], "26m", False),
            ("Storytelling with Metrics", "Grafiklar va xulosalarni stakeholder tili bilan taqdim etamiz.", "https://www.youtube.com/watch?v=Gp4ZpkNnSRI", UNSPLASH["mentor"], "22m", False),
        ],
    },
]

TESTIMONIAL_DATA = [
    {
        "name": "Dilnoza Karimova",
        "role": "Junior Backend Developer, Tashkent",
        "quote": "Asilbek aka kurslari menga faqat syntax emas, product thinking ham berdi. REST API kursidan keyin interviewlarda ancha ishonch bilan gapira boshladim va ikki oy ichida ishga kirdim.",
        "avatar_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=400&q=80",
        "rating": Decimal("5.0"),
        "sort_order": 1,
    },
    {
        "name": "Jahongir Raximov",
        "role": "Computer Science Student",
        "quote": "Oldin Pythonni o'zimcha o'qib yurgandim, lekin roadmap yo'q edi. Bu platformada darslar tartibli, vazifalar real va o'qitish uslubi juda tushunarli. Endi portfolio yig'ishni boshladim.",
        "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80",
        "rating": Decimal("4.9"),
        "sort_order": 2,
    },
    {
        "name": "Madina Yuldasheva",
        "role": "QA Engineer transitioning to Backend",
        "quote": "Django Fullstack Mastery kursida menga yoqqani - hamma narsa productga bog'lab tushuntiriladi. Shunchaki model va view emas, nima uchun bu yechim biznesda ishlashini ham ko'rasiz.",
        "avatar_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=400&q=80",
        "rating": Decimal("5.0"),
        "sort_order": 3,
    },
    {
        "name": "Ethan Brooks",
        "role": "Freelance Web Developer",
        "quote": "The strongest part of EduPlanet is how practical the material feels. I expected another theory-heavy course, but instead I got reusable patterns, deployment checklists, and better confidence when shipping client work.",
        "avatar_url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=400&q=80",
        "rating": Decimal("4.8"),
        "sort_order": 4,
    },
    {
        "name": "Shohruh Tursunov",
        "role": "DevOps Intern",
        "quote": "DevOps Basics kursi menga Docker va CI/CD'ni backend nuqtayi nazaridan tushunishga yordam berdi. Endi deploy jarayonidan qo'rqmayman va jamoa ichida ko'proq mas'uliyat ola boshladim.",
        "avatar_url": "https://images.unsplash.com/photo-1504593811423-6dd665756598?auto=format&fit=crop&w=400&q=80",
        "rating": Decimal("4.9"),
        "sort_order": 5,
    },
    {
        "name": "Anna Petrova",
        "role": "Product Analyst",
        "quote": "Data Science Foundations course helped me understand metrics and datasets much better. I can now talk to engineering teams with more confidence because the examples were business-oriented, not abstract.",
        "avatar_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=400&q=80",
        "rating": Decimal("4.8"),
        "sort_order": 6,
    },
]

INSTRUCTOR_DATA = {
    "username": "asilbek",
    "email": "asilbekmirolimov@gmail.com",
    "first_name": "Asilbek",
    "last_name": "Mirolimov",
    "title": "Senior Software Engineer & Educator",
    "bio": "Asilbek Mirolimov - 5+ yillik tajribaga ega Senior Software Engineer va educator. U Python, Django, REST API, PostgreSQL va DevOps basics yo'nalishlarida product-focused tizimlar yaratib keladi. Faoliyati davomida startup MVP'lardan ichki admin platformalargacha bo'lgan yechimlarni ishlab chiqqan, jamoalar ichida architecture, delivery va code quality standartlarini shakllantirgan. EduPlanet orqali u nazariyani emas, real product tajribani o'rgatishni maqsad qilgan.",
    "mission": "O'zbekistondan global bozorda raqobat qila oladigan backend engineerlar va builderlar avlodini tayyorlash - sodda tushuntirish, real loyihalar va yuqori standartli mentorlik orqali.",
    "profile_description": "Asilbekning darslari backend engineering, product thinking va career growthni birlashtiradi. Kurslar juniorlardan boshlab ishlayotgan developerlargacha mo'ljallangan bo'lib, har bir modul ishga tayyor skill hosil qilishga qaratilgan.",
    "experience_years": 5,
    "skills": ["Python", "Django", "REST API", "PostgreSQL", "DevOps basics"],
    "location": "Tashkent, Uzbekistan",
    "website": "https://eduplanet.uz",
    "linkedin": "https://www.linkedin.com/in/asilbekmirolimov/",
    "github": "https://github.com/asilbek3450",
    "telegram": "https://t.me/mirolimov_a",
    "avatar_url": UNSPLASH["mentor"],
    "translations": {
        "bio": {
            "uz": "Asilbek Mirolimov - 5+ yillik tajribaga ega Senior Software Engineer va educator. U Python, Django, REST API, PostgreSQL va DevOps basics yo'nalishlarida product-focused tizimlar yaratib keladi. Faoliyati davomida startup MVP'lardan ichki admin platformalargacha bo'lgan yechimlarni ishlab chiqqan, jamoalar ichida architecture, delivery va code quality standartlarini shakllantirgan. EduPlanet orqali u nazariyani emas, real product tajribani o'rgatishni maqsad qilgan.",
            "en": "Asilbek Mirolimov is a Senior Software Engineer and educator with 5+ years of experience building product-focused systems with Python, Django, REST APIs, PostgreSQL, and DevOps basics. He has shipped startup MVPs, internal admin platforms, and growth-oriented features while shaping architecture, delivery standards, and code quality inside teams. Through EduPlanet, he teaches practical product experience rather than isolated theory.",
            "ru": "Асилбек Миролимов — Senior Software Engineer и преподаватель с 5+ годами опыта в Python, Django, REST API, PostgreSQL и DevOps basics. Он запускал startup MVP, внутренние admin-платформы и growth features, формируя architecture, delivery standards и code quality в командах. Через EduPlanet он делает ставку не на изолированную теорию, а на реальный product experience.",
        },
        "mission": {
            "uz": "O'zbekistondan global bozorda raqobat qila oladigan backend engineerlar va builderlar avlodini tayyorlash - sodda tushuntirish, real loyihalar va yuqori standartli mentorlik orqali.",
            "en": "To help build a new generation of backend engineers and builders from Uzbekistan who can compete globally through clear teaching, real projects, and high-standard mentorship.",
            "ru": "Готовит новое поколение backend-инженеров и builders из Узбекистана, которые могут конкурировать глобально, через понятное объяснение, реальные проекты и высокие стандарты менторства.",
        },
        "profile_description": {
            "uz": "Asilbekning darslari backend engineering, product thinking va career growthni birlashtiradi. Kurslar juniorlardan boshlab ishlayotgan developerlargacha mo'ljallangan bo'lib, har bir modul ishga tayyor skill hosil qilishga qaratilgan.",
            "en": "Asilbek's teaching combines backend engineering, product thinking, and career growth. The programs are built for beginners through working developers, and each module aims to create job-ready skills.",
            "ru": "Подход Асилбека объединяет backend engineering, product thinking и career growth. Программы подходят и новичкам, и работающим разработчикам, а каждый модуль ведет к job-ready навыкам.",
        },
        "title": {"uz": "Senior Software Engineer & Educator", "en": "Senior Software Engineer & Educator", "ru": "Senior Software Engineer и преподаватель"},
    },
}


def build_article_html(title, intro, sections, conclusion):
    parts = [f"<h1>{title}</h1>", f"<p>{intro}</p>"]
    for section in sections:
        parts.append(f"<h2>{section['heading']}</h2>")
        for paragraph in section["paragraphs"]:
            parts.append(f"<p>{paragraph}</p>")
        for subsection in section.get("subsections", []):
            parts.append(f"<h3>{subsection['heading']}</h3>")
            for paragraph in subsection["paragraphs"]:
                parts.append(f"<p>{paragraph}</p>")
    parts.append(f"<p>{conclusion}</p>")
    return "\n".join(parts)


BLOG_DATA = [
    {
        "title": "Pythonni 2025-yilda qanday o'rganish kerak: noldan ishga tayyor roadmap",
        "slug": "pythonni-2025-yilda-qanday-organish-kerak",
        "excerpt": "Python course Uzbekistan qidirayotganlar uchun roadmap, amaliy portfolio va o'qish tartibini ko'rsatadigan chuqur qo'llanma.",
        "cover_image": UNSPLASH["python"],
        "topic": "Python Learning",
        "reading_time": 8,
        "seo_title": "Pythonni 2025-yilda qanday o'rganish kerak | Python course Uzbekistan",
        "seo_description": "Python course Uzbekistan qidirayotganlar uchun amaliy roadmap: sintaksis, portfolio, project va ishga tayyorlanish bosqichlari.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["How to learn Python in 2025", "python roadmap", "python darslari toshkent"]),
        "published_at": date(2026, 3, 4),
        "featured": True,
        "content": build_article_html(
            "Pythonni 2025-yilda qanday o'rganish kerak",
            "Python hanuz eng kuchli start nuqtalardan biri bo'lib qolmoqda. Sun'iy intellekt, backend development, automation va analytics kabi bir nechta yo'nalishlarda bir xil til ishlatilayotgani sababli, yangi boshlovchi uchun ham, yo'nalishini o'zgartirmoqchi bo'lgan mutaxassis uchun ham Python oqilona tanlov. Ammo muammo odatda tilning o'zida emas - uni qanday tartibda o'rganishda. Ko'pchilik random videolar, bir-biriga ulanmagan tutoriallar va haddan tashqari ko'p resurslar orasida yo'lini yo'qotadi. To'g'ri roadmap bo'lsa, 6-8 oy ichida ishga tayyor darajaga yetishish mumkin.",
            [
                {
                    "heading": "1. Avval maqsadni aniqlang: backend, automation yoki data?",
                    "paragraphs": [
                        "Pythonni o'rganishni boshlashdan oldin o'zingizga bitta aniq savol bering: men bu til bilan nima qilmoqchiman? Kimdir web backendga kiradi, boshqasi automation skriptlari yozadi, yana kimdir data science tomonga qiziqadi. Yo'nalish aniq bo'lmasa, resurs tanlash ham qiyinlashadi va o'quv jarayoni uzoq cho'ziladi.",
                        "Agar maqsad backend bo'lsa, syntaxdan keyin Django, REST API va PostgreSQLga o'tasiz. Automation uchun files, APIs va scheduling ko'proq ahamiyatli bo'ladi. Data yo'nalishi uchun esa pandas, notebooks va statistik fikrlash kerak bo'ladi. Birinchi kundan maqsadni bilish - keraksiz chalg'ishlarni kamaytiradi.",
                    ],
                    "subsections": [
                        {
                            "heading": "Birinchi 30 kun uchun tavsiya",
                            "paragraphs": [
                                "Dastlabki oyda syntax, loops, functions, lists, dicts va file handling yetarli. Bu davrda mukammallikka emas, tushunishga e'tibor qarating. Har yangi mavzu uchun kamida bitta mini mashq qiling: kalkulyator, to-do manager, CSV parser yoki Telegram bot kabi kichik amaliyotlar juda foydali.",
                            ],
                        }
                    ],
                },
                {
                    "heading": "2. Syntaxni project bilan birga o'rganing",
                    "paragraphs": [
                        "Ko'p boshlovchilar xato qiladi: ular avval butun nazariyani tugatmoqchi bo'ladi, keyin project boshlashni rejalashtiradi. Amalda esa projectning o'zi nazariyani mustahkamlaydi. Agar siz faqat videoni ko'rib ketsangiz, bir haftadan keyin unutish boshlanadi. Agar shu mavzuni darhol kichik productga aylantirsangiz, bilim tezroq qoladi.",
                        "Masalan, dictionaries o'rgangan zahoti expense tracker qiling. Requests kutubxonasini ko'rgach weather API iste'mol qiling. Functions mavzusidan keyin reusable utility module yozing. O'qish va qilish birga ketganda, Python qo'rqinchli ko'rinmaydi va siz 'men ishlatib ko'rdim' degan ishonchni yig'asiz.",
                    ],
                },
                {
                    "heading": "3. GitHub portfolio erta boshlansin",
                    "paragraphs": [
                        "Ishga kirish uchun faqat kurs sertifikati yetmaydi. Ish beruvchi yoki mentor sizning qanday fikrlashingizni, kodni qanday tartiblashingizni va qancha mustaqil ishlay olishingizni ko'rmoqchi bo'ladi. Shu sabab GitHub portfolio Python o'rganishning yakuniy qismi emas - jarayonning o'zidir.",
                        "Har ikki yoki uch haftada bir mini project joylang. README yozing, texnologiyalarni sanang, qaysi muammoni hal qilganingizni tushuntiring. Hatto oddiy CLI app bo'lsa ham, u sizning intizomingiz va amaliy yondashuvingizni ko'rsatadi. Portfolio vaqt o'tishi bilan o'ssa, o'zingiz ham taraqqiyot yo'lini aniq ko'rasiz.",
                    ],
                },
                {
                    "heading": "4. Roadmap: Python -> Django -> API -> Database",
                    "paragraphs": [
                        "Agar siz backend developer bo'lmoqchi bo'lsangiz, roadmapni ortiqcha murakkablashtirmang. Avval Python fundamentals, keyin OOP basics, undan keyin Django. Django bilan birga HTTP, forms, auth va template tushunchalarini egallang. Shundan keyin Django REST Framework va PostgreSQL bilan API hamda database design ustida ishlash mumkin.",
                        "Bu ketma-ketlik juda muhim, chunki har bosqich keyingisiga tayanch bo'ladi. Syntaxni to'g'ri tushunmagan odam framework ichida yo'qolib qoladi. Database haqida tasavvuri yo'q developer esa API dizaynida qiynaladi. Qisqasi, tartibni saqlash tezlikni oshiradi.",
                    ],
                },
            ],
            "Xulosa shuki, Pythonni 2025-yilda o'rganish uchun ko'proq resurs emas, ko'proq aniqlik kerak. Bitta yo'nalish tanlang, syntaxni projectlar bilan birlashtiring, GitHub portfolio'ni erta boshlang va o'quv yo'lini ketma-ket olib boring. Shunda Python course Uzbekistan yoki backend course Tashkent kabi qidiruvlardan chiqqan resurslar ichida adashmay, real natijaga tezroq yetasiz.",
        ),
    },
    {
        "title": "Django vs Flask: qaysi framework siz uchun to'g'ri?",
        "slug": "django-vs-flask-qaysi-framework",
        "excerpt": "Django vs Flask tanlovida eng muhim mezonlar: product complexity, jamoa talabi, delivery tezligi va long-term maintainability.",
        "cover_image": UNSPLASH["backend"],
        "topic": "Framework Comparison",
        "reading_time": 7,
        "seo_title": "Django vs Flask | Qaysi frameworkni tanlash kerak?",
        "seo_description": "Django va Flask o'rtasidagi tanlovni product complexity, jamoa hajmi va delivery tezligi nuqtayi nazaridan tahlil qilamiz.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["Django vs Flask", "Python web framework", "backend roadmap"]),
        "published_at": date(2026, 3, 2),
        "featured": True,
        "content": build_article_html(
            "Django vs Flask: qaysi framework siz uchun to'g'ri?",
            "Python web developmentga kirganlar juda tez bitta savolga duch keladi: Django ishlataymi yoki Flaskmi? Ikkalasi ham mashhur, ikkalasi ham productionda ishlatiladi, lekin ular bir xil vazifa uchun yaratilmagan. Django ko'proq 'batareyasi ichida' bo'lgan framework bo'lsa, Flask minimal va erkin yondashuvni taklif qiladi. Shuning uchun tanlov faqat sintaksisga emas, product ehtiyojiga bog'liq bo'lishi kerak.",
            [
                {
                    "heading": "1. Django tezroq product chiqarish uchun kuchli",
                    "paragraphs": [
                        "Agar sizda auth, admin panel, forms, ORM, templating va user management kerak bo'lsa, Django katta ustunlik beradi. Bu narsalar alohida-alohida o'ylab topilmaydi, framework ichida yaxshi tayyorlangan holda keladi. Startup MVP yoki ichki boshqaruv paneli uchun bu juda katta vaqt yutug'i.",
                        "Shuningdek, Django jamoa ichida standartlarni yaxshi ushlab turadi. Yangi developer kelsa, kod bazasida qayerda nima bo'lishini tezroq tushunadi. Long-term maintainability nuqtayi nazaridan bu juda muhim. Aynan shu sabab ko'plab ta'lim, SaaS va admin-heavy productlar uchun Django hali ham kuchli tanlov.",
                    ],
                },
                {
                    "heading": "2. Flask moslashuvchan, lekin qarorlar sizga qoladi",
                    "paragraphs": [
                        "Flaskning eng katta afzalligi - yengilligi. Kichik servis, custom architecture yoki faqat API yozmoqchi bo'lsangiz, Flask sizni ortiqcha qoidalarga majbur qilmaydi. Bu tajribali muhandis uchun qulay bo'lishi mumkin, ayniqsa mahsulot juda spetsifik bo'lsa.",
                        "Ammo bu erkinlikning narxi bor. Siz auth qanday bo'ladi, admin kerakmi, project structure qanaqa bo'ladi, migrations va extensionsni qanday boshqarasiz - barchasini o'zingiz hal qilasiz. Tajriba kam bo'lsa, bu erkinlik tezda tartibsizlikka aylanishi mumkin.",
                    ],
                },
                {
                    "heading": "3. O'rganish nuqtayi nazaridan qaysi biri yaxshiroq?",
                    "paragraphs": [
                        "Boshlovchi uchun Flask soddaroqdek ko'rinadi, chunki kod kamroq va conceptlar kamroq ko'rinadi. Lekin ish bozoriga qarasak, ayniqsa Uzbekistan va Tashkent atrofidagi backend vakansiyalarda Django ko'proq uchraydi. Demak, o'rganishdagi soddalik bilan ishga tayyorlik har doim bir xil narsa emas.",
                        "Agar maqsad backend career bo'lsa, Django ko'proq 'full product understanding' beradi. Agar maqsad mikrosservislar yoki kichik internal tools bo'lsa, Flask foydali bo'lishi mumkin. Muhimi, frameworkni emas, o'sha framework sizni qaysi skillga olib borishini tanlang.",
                    ],
                },
                {
                    "heading": "4. Qisqa xulosa: productdan kelib chiqing",
                    "paragraphs": [
                        "Agar siz tezda course platform, CRM, dashboard, blog yoki marketplace kabi product yig'moqchi bo'lsangiz, Django ko'proq foyda beradi. Agar siz aniq bir API servisi yoki custom lightweight service qursangiz, Flask mantiqli bo'lishi mumkin.",
                        "Tanlovni faqat 'qaysi biri mashhur' degan savol bilan qilmang. Jamoa hajmi, product scope, vaqt, maintainability va o'zingizning tajriba darajangizga qarang. Shunda Django vs Flask savoli chalkashlik emas, strategik qarorga aylanadi.",
                    ],
                },
            ],
            "Shu bois aksariyat junior backend developerlar uchun Django yaxshi boshlanish nuqtasi bo'lib qolmoqda. U product architecture, database, auth va user workflowsni bir joyda ko'rsatadi. Flask esa keyinroq, muayyan ehtiyoj paydo bo'lganda o'rganilsa ham bo'ladi. Framework tanlashning eng to'g'ri usuli - o'zingiz qurmoqchi bo'lgan mahsulotga qarash.",
        ),
    },
    {
        "title": "Backend developer roadmap: boshlovchidan ishga tayyor darajagacha",
        "slug": "backend-developer-roadmap-boshlovchidan-ishga-tayyor",
        "excerpt": "Backend roadmap chalkash bo'lib ko'rinsa ham, to'g'ri ketma-ketlik bilan uni boshqarish oson: Python, HTTP, Django, API, SQL va deployment.",
        "cover_image": UNSPLASH["server"],
        "topic": "Career Growth",
        "reading_time": 8,
        "seo_title": "Backend developer roadmap | Ishga tayyor bo'lish uchun aniq yo'l",
        "seo_description": "Python, HTTP, Django, REST API, SQL va deployment bosqichlari orqali junior developer uchun aniq backend roadmap.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["backend roadmap", "backend developer roadmap", "backend course tashkent"]),
        "published_at": date(2026, 2, 26),
        "featured": True,
        "content": build_article_html(
            "Backend developer roadmap: boshlovchidan ishga tayyor darajagacha",
            "Backend development ko'pchilikka noaniq ko'rinadi, chunki u bir vaqtning o'zida dasturlash, database, architecture va deploymentni o'z ichiga oladi. Shu sabab ko'plab boshlovchilar nimadan boshlashni bilmaydi yoki juda erta murakkab mavzularga sakrab ketadi. Aslida esa backend roadmap juda aniq: syntaxdan boshlanadi, product thinking bilan tugaydi. To'g'ri ketma-ketlikni ushlasangiz, progress tezroq seziladi.",
            [
                {
                    "heading": "1. Birinchi qatlam: Python va problem solving",
                    "paragraphs": [
                        "Backendga kirish uchun avval bitta til bilan qulaylik hosil qilish kerak. Python bu vazifa uchun juda mos, chunki sintaksisi o'qilishi oson va learning curve nisbatan yumshoq. Ammo maqsad faqat tilni yodlash emas, muammoni kod bilan ifodalashni o'rganish bo'lishi kerak.",
                        "Loops, functions, lists, dicts, files va exceptions bilan ishlash orqali siz dasturlash muskulini shakllantirasiz. Shu bosqichda mini CLI tools va API consumer'lar yozish juda foydali. Bu foundation keyingi framework bosqichida sizni ancha tezlashtiradi.",
                    ],
                },
                {
                    "heading": "2. HTTP, request-response va web fundamentals",
                    "paragraphs": [
                        "Ko'p odam Django yoki Flaskga darhol o'tadi, lekin HTTP'ni tushunmasdan framework faqat sehrli quti bo'lib ko'rinadi. Request, response, headers, methods, status codes va cookies kabi tushunchalarni amalda o'rganing. Bu bilim API va auth bilan ishlaganda juda katta foyda beradi.",
                        "Aynan shu joyda browser qanday ishlashi, form submit nima qilishi, session nimani saqlashi va REST nima ekanini yaxshiroq anglaysiz. Backend engineer uchun bu bilim optional emas, asosdir. Chunki framework o'zgarishi mumkin, lekin internetning asosiy modeli o'zgarmaydi.",
                    ],
                },
                {
                    "heading": "3. Django yoki tanlangan framework ichida product qurish",
                    "paragraphs": [
                        "Framework bosqichida siz user auth, ORM, templates, admin, routing va forms bilan ishlaysiz. Bu stage'da maqsad - o'zingizni tool ichida yo'qotish emas, real use-case qurish. Blog, course platform, booking app yoki CRM'ga o'xshash product tanlang. Qachonki conceptlar real ob'ektlar bilan bog'lansa, o'rganish tezlashadi.",
                        "Shu yerda clean structure, naming va modularity odatlari ham shakllanadi. Keyinchalik ishga kirganingizda aynan shu odatlar sizni ajratib turadi. Junior darajada ham yaxshi foundation ko'rinib turadi.",
                    ],
                },
                {
                    "heading": "4. API, SQL va deployment - ishga tayyorlik signali",
                    "paragraphs": [
                        "Ish bozorida kuchli signal beradigan skilllar - REST API yozish, SQLni tushunish va ilovani deploy qila olish. API sizni frontend yoki mobile jamoa bilan ulaydi. SQL esa product ma'lumotlari bilan fikrlashni o'rgatadi. Deployment esa operational confidence beradi.",
                        "Shu uchala qatlamni portfolioga qo'shsangiz, siz oddiy 'kurs ko'rgan talaba' emas, real product bilan ishlashga yaqin developer ko'rinasiz. Backend roadmapning yakuni aynan shu: ishlaydigan, deploy bo'lgan va boshqalar foydalanishi mumkin bo'lgan loyiha.",
                    ],
                },
            ],
            "Backend developer bo'lish sir emas - bu ketma-ketlik masalasi. Python bilan foundation qo'ying, web fundamentalsni tushuning, Django yoki boshqa framework bilan product quring, so'ng API, SQL va deploymentni qo'shing. Har bosqichda amaliy loyiha bo'lsa, ishga tayyorlik hissi juda tez paydo bo'ladi.",
        ),
    },
    {
        "title": "Qanday qilib developer bo'lish mumkin: 9 bosqichli real plan",
        "slug": "qanday-qilib-developer-bolish-mumkin",
        "excerpt": "Developer bo'lish uchun supertalant emas, tizimli reja, muntazam practice va to'g'ri muhit kerak.",
        "cover_image": UNSPLASH["team"],
        "topic": "Career Growth",
        "reading_time": 7,
        "seo_title": "Qanday qilib developer bo'lish mumkin | 9 bosqichli plan",
        "seo_description": "Developer bo'lish uchun aniq 9 bosqichli reja: yo'nalish tanlash, portfolio, networking va job search taktikalari.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["how to become a developer", "developer bolish", "programming journey"]),
        "published_at": date(2026, 2, 20),
        "featured": False,
        "content": build_article_html(
            "Qanday qilib developer bo'lish mumkin: 9 bosqichli real plan",
            "Developer bo'lish ko'p odamga uzoq va chalkash ko'rinadi. Go'yo faqat matematika biladigan yoki juda erta boshlagan odamlar bu yo'lga kira oladigandek tuyuladi. Aslida esa bu kasbga kirishda eng katta farqni iste'dod emas, tizim beradi. Agar siz yo'nalishni to'g'ri tanlasangiz, muntazam practice qilsangiz va o'zingizni bozorga to'g'ri ko'rsata olsangiz, natija keladi.",
            [
                {
                    "heading": "1. Yo'nalish tanlang va 3 oyga sodiq qoling",
                    "paragraphs": [
                        "Birinchi xato - har hafta yangi yo'nalishga o'tish. Bugun frontend, ertaga AI, keyin mobile. Bu sizni motivatsiya yuqori bo'lsa ham, natijadan uzoqlashtiradi. Dastlab bir yo'nalishni tanlang va kamida 90 kun shu yo'nalishda qoling.",
                        "Agar siz product systems, database va APIsga qiziqsangiz, backend yaxshi tanlov. Agar UI va visual tomonni yaxshi ko'rsangiz, frontend. Muhimi, tanlov qilgach o'zingizni taqqoslashdan ko'ra, skill yig'ishga e'tibor bering.",
                    ],
                },
                {
                    "heading": "2. Kurs + practice + feedback uchligini yarating",
                    "paragraphs": [
                        "Faqat kurs ko'rish yetmaydi. Faqat mustaqil mashq ham ko'pincha samarasiz bo'ladi. Eng yaxshi kombinatsiya - tartibli o'quv materiali, doimiy amaliyot va vaqtida feedback olish. Chunki ko'p xatolarni inson o'zi sezmaydi.",
                        "Mentor yoki community bo'lsa, bu jarayon tezlashadi. Savol berishdan uyalmang. Yaxshi savol berishning o'zi ham developer skill hisoblanadi. Eng muhimi, har hafta tangible natija bo'lsin: commit, project yoki demo.",
                    ],
                },
                {
                    "heading": "3. Portfolio va networking ish qidirishdan oldin boshlansin",
                    "paragraphs": [
                        "Ko'pchilik portfolio'ni faqat ish qidirishda eslaydi. Bu kech. Aslida portfolio o'qish davomida yig'ilishi kerak. GitHub, LinkedIn va 2-3 ta yaxshi izohlangan loyiha sizning professional signalizatsiyangiz bo'ladi.",
                        "Networking ham faqat tanish orttirish emas. Community ichida ko'rinish, foydali post yozish, boshqalarning savollariga javob berish va o'zingizning progressni ko'rsatish - bularning barchasi ish topish ehtimolini oshiradi. Ish beruvchi ko'pincha faol va sistemali odamni ko'rishni xohlaydi.",
                    ],
                },
                {
                    "heading": "4. Ishga tayyorlik - mukammallik emas, foydalilik",
                    "paragraphs": [
                        "Developer bo'lish uchun hamma narsani bilish shart emas. Ishga tayyor bo'lish degani - siz muammoni tahlil qila olasiz, yordam so'rashni bilasiz, documentation o'qiysiz va mavjud kod ichida value bera olasiz. Junior position aynan shuni kutadi.",
                        "Shuning uchun 'yana biroz o'rganay, keyin boshlayman' degan holatda uzoq qolmang. Ma'lum bir nuqtadan keyin bozorga chiqishning o'zi o'qishning bir qismiga aylanadi. Real interview va test tasklar ham sizni o'stiradi.",
                    ],
                },
            ],
            "Developer bo'lish uchun super qobiliyat kerak emas. Aniqlik, muntazamlik va amaliy natija kerak. Yo'nalishni tanlang, 3 oyga sodiq qoling, kurs va practice'ni birlashtiring, portfolio'ni erta boshlang va bozorga chiqishdan qo'rqmang. Shunda bu yo'l tasavvurdagidan ancha real va boshqariladigan bo'lib qoladi.",
        ),
    },
    {
        "title": "Django REST Framework bilan production API qurish bo'yicha amaliy qo'llanma",
        "slug": "django-rest-framework-production-api-qollanma",
        "excerpt": "Serializer, auth, permissions, errors va docs bo'yicha mustahkam qarorlar production API sifatini belgilaydi.",
        "cover_image": UNSPLASH["server"],
        "topic": "Backend Engineering",
        "reading_time": 8,
        "seo_title": "Django REST Framework bilan production API qurish",
        "seo_description": "Production API uchun serializer design, permissions, pagination, docs va error handling bo'yicha amaliy qo'llanma.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["Django REST Framework", "production api", "REST API guide"]),
        "published_at": date(2026, 2, 14),
        "featured": False,
        "content": build_article_html(
            "Django REST Framework bilan production API qurish bo'yicha amaliy qo'llanma",
            "DRF bilan API yozish oson boshlanadi. Serializer, viewset va router qo'shasiz - endpoint ishlaydi. Ammo production darajada ishonchli API qurish uchun bundan ko'proq narsa kerak. Consumer tajribasi, predictable errors, documentation, versioning va permissions kabi qatlamlar sifatni belgilaydi. Shu jihatlar e'tibordan chetda qolsa, API ishlasa ham, product jamoa uchun qimmatga tushadi.",
            [
                {
                    "heading": "1. Resource design - endpointdan oldin model o'ylang",
                    "paragraphs": [
                        "Yaxshi API naming va resource modelingdan boshlanadi. URL qanday ko'rinishi, qaysi fieldlar qaytishi va consumer qanday flow bilan foydalanishi avval o'ylab chiqilishi kerak. Aks holda tez yozilgan endpointlar keyin birdan murakkab bo'lib qoladi.",
                        "Masalan, enroll, payment, profile update va dashboard metrics kabi flowlar har xil resurslarga tayanadi. Ularni bitta 'mega endpoint'ga siqish o'rniga aniq javobgarlik bilan ajrating. Shunda frontend va mobile jamoa uchun API ancha tushunarli bo'ladi.",
                    ],
                },
                {
                    "heading": "2. Permissions va auth - keyin emas, boshida",
                    "paragraphs": [
                        "Ko'p loyihalarda auth va permissions keyin qo'shiladi. Natijada kod ko'paygach, access logic tarqalib ketadi. Production APIda esa bu qatlam boshidan dizayn qilinishi kerak. Kim nimani ko'ra oladi, kim nimani yaratadi, qaysi endpoint public - aniq qoida bo'lishi zarur.",
                        "DRF bu yerda kuchli imkoniyat beradi: custom permissions, authentication backends va object-level checks. Foydalanishni to'g'ri tashkil qilsangiz, business rulesni view ichida if bilan to'ldirishga ehtiyoj kamayadi.",
                    ],
                },
                {
                    "heading": "3. Predictable error responses va documentation",
                    "paragraphs": [
                        "Consumer-friendly API faqat muvaffaqiyatli response bilan o'lchanmaydi. Xatolar qanchalik tushunarli ekanligi ham juda muhim. Agar frontend biror xatoni ushlaganda nima qilishni bilmasa, product tajribasi zarar ko'radi. Shu sabab error contract iloji boricha bir xil formatda bo'lishi kerak.",
                        "Documentation ham shu darajada muhim. Swagger yoki Redoc bo'lsin, lekin example payload, auth requirement va response formatlar aniq ko'rsatilishi zarur. Bu nafaqat boshqa jamoalar, balki kelajakdagi o'zingiz uchun ham katta yengillik.",
                    ],
                },
                {
                    "heading": "4. Performance va paginationni erta o'ylang",
                    "paragraphs": [
                        "API boshida kichik dataset bilan ishlaydi va tez ko'rinadi. Keyin data ko'paygach, list endpointlar sekinlashadi, nested serializerlar shishib ketadi va DB load ortadi. Shu sabab pagination, select_related, prefetch_related va selective fields strategiyasini erta joriy qilish foydali.",
                        "Performance muammolari juda ko'p hollarda architecture qarorlaridan kelib chiqadi. Yaxshi production API nafaqat to'g'ri javob beradi, balki buni barqaror tezlikda ham qila oladi.",
                    ],
                },
            ],
            "Production API qurish - bu endpointlarni ko'paytirish emas, product ishonchini qurishdir. Resource design, auth, predictable errors, docs va performancega boshidan e'tibor bersangiz, DRF kuchli asos beradi. Aynan shu yondashuv API'ni jamoa uchun foydali, boshqariladigan va o'sishga tayyor holatga keltiradi.",
        ),
    },
    {
        "title": "PostgreSQL performance tuning: Django ilovalarda eng ko'p foyda beradigan 7 usul",
        "slug": "postgresql-performance-tuning-django",
        "excerpt": "Slow querylarni kamaytirish uchun query plan, indexes va ORM usage'ga birgalikda qarash kerak.",
        "cover_image": UNSPLASH["server"],
        "topic": "Database",
        "reading_time": 7,
        "seo_title": "PostgreSQL performance tuning for Django apps",
        "seo_description": "Django ilovalarida PostgreSQL performance tuning uchun index, query plan va ORM usage bo'yicha 7 amaliy tavsiya.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["PostgreSQL tuning", "Django performance", "database optimization"]),
        "published_at": date(2026, 2, 8),
        "featured": False,
        "content": build_article_html(
            "PostgreSQL performance tuning: Django ilovalarda eng ko'p foyda beradigan 7 usul",
            "Django ilovada sekinlik ko'rinsa, ko'pchilik darhol server yoki caching haqida o'ylaydi. Aslida esa muammo ko'pincha database bilan qanday muloqot qilayotganimizda bo'ladi. Notog'ri relationlar, ortiqcha queries, indekssiz filtering yoki katta response payloadlar performance'ni sezilarli yomonlashtiradi. Yaxshi xabar shundaki, ko'p hollarda katta o'zgarishsiz ham yaxshi natija olish mumkin.",
            [
                {
                    "heading": "1. Avval query plan'ni ko'ring",
                    "paragraphs": [
                        "Optimizatsiya qilishdan oldin muammoni ko'rish kerak. PostgreSQL'da EXPLAIN va EXPLAIN ANALYZE so'rovingiz qayerda vaqt ketayotganini aniq ko'rsatadi. Ko'p developerlar buni o'tkazib yuborib, taxmin bilan ishlaydi. Natijada muammo qolaveradi yoki boshqa joyda paydo bo'ladi.",
                        "Query planni o'qishni odat qilsangiz, sequential scan, bad join order yoki missing index kabi muammolar tezroq ko'rinadi. Bu skill database bilan ishlashda eng katta leverage beradi.",
                    ],
                },
                {
                    "heading": "2. Indexlar hamma joyda emas, kerakli joyda bo'lsin",
                    "paragraphs": [
                        "Index qo'shish foydali, lekin har fieldga index qo'yish yaxshi amaliyot emas. Siz ko'p filter qiladigan, join qiladigan yoki order by ishlatadigan ustunlarni aniqlab, aynan o'sha joylarda index qo'yishingiz kerak. Aks holda writes sekinlashadi va storage ortadi.",
                        "Django model darajasida index qo'shish oson, lekin product usage'dan kelib chiqib qaror qiling. Performance tuning - ma'lumotga qarab qilingan engineering qarori.",
                    ],
                },
                {
                    "heading": "3. ORM convenience ba'zan qimmatga tushadi",
                    "paragraphs": [
                        "Django ORM juda qulay, lekin hamma qulay narsalar arzon bo'lavermaydi. N+1 querylar, keraksiz selectlar va ortiqcha nested serialization ko'p loyihada asosiy sekinlik manbai bo'ladi. select_related va prefetch_related bu yerda eng oddiy, lekin eng katta foyda beradigan usullardan.",
                        "Shuningdek, faqat kerakli fieldlarni olish, annotate bilan aggregation qilish va list endpointlarni ehtiyotkor yozish kerak. ORM'ni sevish mumkin, lekin uning narxini bilgan holda ishlatish kerak.",
                    ],
                },
                {
                    "heading": "4. Reporting va analytics uchun alohida strategiya qiling",
                    "paragraphs": [
                        "Operational queries bilan reporting queries har doim ham bir xil emas. Product ichidagi tezkor response talab qiladigan endpoint bilan katta dashboard report bir xil tarzda ishlamasligi kerak. Ba'zi hollarda materialized view, periodic aggregation yoki summary table ancha to'g'ri bo'ladi.",
                        "Agar siz hamma narsani real-time qilishga urinsangiz, database ortiqcha yuk ostida qoladi. Product nuqtayi nazaridan qaysi ma'lumot haqiqatan ham real-time bo'lishi kerakligini ajrating.",
                    ],
                },
            ],
            "Django ilovalarda performance ko'p hollarda ORM va PostgreSQL o'rtasidagi chegara nuqtasida yotadi. Query plan, to'g'ri indekslar, ehtiyotkor ORM usage va reporting strategiyasi orqali katta yutuqlar qilish mumkin. Backend engineer uchun bu bilim ish unumdorligini ham, product sifatini ham oshiradi.",
        ),
    },
    {
        "title": "Junior dasturchilar qiladigan 10 ta xato va ularni qanday to'g'rilash mumkin",
        "slug": "junior-dasturchilar-qiladigan-xatolar",
        "excerpt": "Ko'p juniorlar syntax emas, learning process va work habits bo'yicha xato qiladi. Ularni erta bilish o'sishni tezlashtiradi.",
        "cover_image": UNSPLASH["workspace"],
        "topic": "Career Growth",
        "reading_time": 7,
        "seo_title": "Junior dasturchilar qiladigan 10 ta xato",
        "seo_description": "Junior developerlar orasida eng keng tarqalgan xatolar va ularni tezroq to'g'rilash bo'yicha amaliy tavsiyalar.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["junior developer mistakes", "developer xatolari", "career growth"]),
        "published_at": date(2026, 2, 1),
        "featured": False,
        "content": build_article_html(
            "Junior dasturchilar qiladigan 10 ta xato va ularni qanday to'g'rilash mumkin",
            "Junior developerning eng katta muammosi bilim yetishmasligi emas. Ko'pincha muammo noto'g'ri yondashuvda bo'ladi. Odam juda ko'p resurs yig'adi, lekin practice qilmaydi. Yoki juda murakkab loyihaga sakraydi, lekin fundamentals mustahkam emas. Yaxshi tomoni shundaki, bu xatolarning aksariyati erta tuzatilsa, o'sish ancha tezlashadi.",
            [
                {
                    "heading": "1. Hamma narsani bir vaqtda o'rganishga urinish",
                    "paragraphs": [
                        "Python, JavaScript, React, Django, Docker, AI - barchasini birdan boshlash juda tanish holat. Bu motivatsiyaning belgisi bo'lishi mumkin, lekin natijada hech biri chuqur o'tirmaydi. Skill stacking foydali, lekin ketma-ket bo'lgandagina foyda beradi.",
                        "Bir davrda bitta asosiy yo'nalish tanlang. Qolganini faqat ko'z tashlash darajasida ushlang. Fokus qanchalik aniq bo'lsa, progress shunchalik seziladi.",
                    ],
                },
                {
                    "heading": "2. Kodni ko'p ko'rib, kam yozish",
                    "paragraphs": [
                        "Video ko'rish va maqola o'qish foydali, lekin ular passiv o'rganish usuli. Kod yozilmasa, skill shakllanmaydi. Ko'p juniorlar 'hammasini tushunib olay, keyin yozaman' deb kutadi. Bu jarayonni sekinlashtiradi.",
                        "Har o'rgangan mavzu bo'yicha kichik amaliy topshiriq bo'lsin. Hatto 20 daqiqalik mashq ham yaxshi. Kod yozish mushak xotirasini shakllantiradi.",
                    ],
                },
                {
                    "heading": "3. Xatodan qochish",
                    "paragraphs": [
                        "Ko'pchilik bug chiqishidan yoki noaniqlikdan qo'rqadi. Natijada yangi narsani sinab ko'rmaydi. Aslida esa xato - feedbackning eng tez ko'rinadigan shakli. Debug qilishni o'rganmagan developer o'sishda qiynaladi.",
                        "Xatoni shaxsiy mag'lubiyat sifatida qabul qilmang. Error message o'qish, print/log qo'yish va documentationga qarash - bular junior uchun eng muhim odatlardan.",
                    ],
                },
                {
                    "heading": "4. Ishga tayyorlikni noto'g'ri talqin qilish",
                    "paragraphs": [
                        "Juniorlar ko'pincha 'men hali tayyor emasman' degan hissiyot bilan juda uzoq qolib ketadi. Ular middle yoki senior darajadagi talablarni o'zidan kutadi. Bu esa ortiqcha bosim beradi.",
                        "Junior tayyorligi - mustaqil o'rganish, savol bera olish, small tasksni yakunlash va jamoa ichida o'sishga tayyor bo'lish demakdir. Mukammallik emas, ishonchli foydalilik kerak.",
                    ],
                },
            ],
            "Junior bosqichdagi eng katta yutuq - xatolarni erta ko'rib, to'g'ri odatlar qurish. Fokusni oshiring, ko'proq kod yozing, xatodan qochmang va ishga tayyorlikni realroq baholang. Shunda o'sish ancha barqaror bo'ladi.",
        ),
    },
    {
        "title": "Clean code nega daromad keltiradi: kod sifati va biznes natijasi o'rtasidagi bog'liqlik",
        "slug": "clean-code-nega-daromad-keltiradi",
        "excerpt": "Clean code faqat estetik masala emas - u delivery tezligi, xato kamayishi va biznes samaradorligiga to'g'ridan-to'g'ri ta'sir qiladi.",
        "cover_image": UNSPLASH["mentor"],
        "topic": "Engineering Quality",
        "reading_time": 6,
        "seo_title": "Clean code nega daromad keltiradi?",
        "seo_description": "Kod sifati, maintainability va delivery tezligi orasidagi real biznes bog'liqligini tahlil qilamiz.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["clean code", "code quality", "business impact"]),
        "published_at": date(2026, 1, 25),
        "featured": False,
        "content": build_article_html(
            "Clean code nega daromad keltiradi: kod sifati va biznes natijasi o'rtasidagi bog'liqlik",
            "Clean code haqida gap ketganda ba'zan bu mavzu faqat seniorlar uchun yoki faqat kod estetikasiga oid deb o'ylashadi. Aslida esa clean code biznes uchun juda amaliy mavzu. Tushunarli, boshqariladigan va test-friendly kod jamoaga tezroq ishlash, kamroq xato qilish va featurelarni xavfsizroq chiqarish imkonini beradi. Bu esa bevosita daromadga ta'sir qiladi.",
            [
                {
                    "heading": "1. Yaxshi kod feature delivery'ni tezlashtiradi",
                    "paragraphs": [
                        "Agar kod bazasi chalkash bo'lsa, har yangi feature katta xavfga aylanadi. Developer avval mavjud logikani tushunishga ko'p vaqt sarflaydi. Kichik o'zgarish ham kutilmagan joyni sindirishi mumkin. Natijada sprint sekinlashadi va business experimentlar kamroq bo'ladi.",
                        "Clean code esa aksincha, kontekstni tezroq ochadi. Funksiya nomlari, modul chegaralari va testlar yaxshi bo'lsa, jamoa tezroq iteratsiya qiladi. Bu bevosita product tezligidir.",
                    ],
                },
                {
                    "heading": "2. Kamroq bug - kamroq support xarajati",
                    "paragraphs": [
                        "Yomon strukturalangan kod bug'larni ko'paytiradi. Bir xatoni tuzatish ikkinchi xatoni chaqirishi mumkin. Bu support, QA va engineering vaqtini yeydi. Clean code esa cause-and-effectni aniqroq ko'rsatadi, debuggingni yengillashtiradi.",
                        "Kamroq incident degani - jamoa energiyasini fire-fighting emas, o'sishga sarflaydi. Biznes uchun bu juda katta farq.",
                    ],
                },
                {
                    "heading": "3. Yangi developerlarni onboard qilish osonlashadi",
                    "paragraphs": [
                        "Kod bazasi tushunarli bo'lsa, yangi muhandis tezroq value bera boshlaydi. Bu hiring xarajatini tezroq qoplaydi. Yangi odam oylar davomida nima bo'layotganini anglashga ketmasdan, real tasklarga ulanadi.",
                        "Aksincha, messy code base ichiga kirgan jamoa a'zosi juda tez charchaydi. Clean code jamoaning operatsion energiyasini saqlaydi.",
                    ],
                },
                {
                    "heading": "4. Investor va founder uchun ham bu signal",
                    "paragraphs": [
                        "Startup kontekstida texnik qarz faqat muhandislarning muammosi emas. Agar product tez o'ssa, yomon kod bazasi biznes modelni ham sekinlashtiradi. Feature chiqish va experiment qilish qimmatlashadi.",
                        "Shuning uchun clean code - bu engineering luxury emas, growth asset. U kichik jamoaning leverage'ini oshiradi va productni uzoqroq masofaga olib boradi.",
                    ],
                },
            ],
            "Demak, clean code nafis ko'rinish uchun emas, tezroq yetkazish va kamroq yo'qotish uchun kerak. Kod sifati bilan biznes natijasi o'rtasida kuchli bog'liqlik bor. Ayniqsa startup yoki tez o'sayotgan jamoalarda bu farq juda tez bilinadi.",
        ),
    },
    {
        "title": "Tajriba bo'lmasa ham kuchli portfolio qanday quriladi?",
        "slug": "tajriba-bolmasa-ham-kuchli-portfolio",
        "excerpt": "Ish tajribasi bo'lmasa ham, to'g'ri tanlangan 3-4 loyiha va aniq izohlangan README sizni kuchli nomzodga aylantiradi.",
        "cover_image": UNSPLASH["workspace"],
        "topic": "Portfolio",
        "reading_time": 7,
        "seo_title": "Portfolio without experience | Kuchli portfolio qanday quriladi?",
        "seo_description": "Tajriba bo'lmasa ham, ishga tayyor developer portfolio'sini yaratish uchun kerakli loyiha va taqdimot tamoyillari.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["portfolio without experience", "github portfolio", "developer portfolio"]),
        "published_at": date(2026, 1, 18),
        "featured": False,
        "content": build_article_html(
            "Tajriba bo'lmasa ham kuchli portfolio qanday quriladi?",
            "Ko'p boshlovchilar 'menda ish tajribasi yo'q, demak portfolio ham kuchsiz bo'ladi' deb o'ylaydi. Aslida portfolio ish joyining o'rnini bosmaydi, lekin u sizning fikrlashingiz, intizomingiz va amaliy odatlaringizni juda yaxshi ko'rsatadi. To'g'ri tanlangan 3-4 loyiha ko'p hollarda 20 ta chala repodan kuchliroq signal beradi.",
            [
                {
                    "heading": "1. Loyiha sonidan ko'ra sifati muhim",
                    "paragraphs": [
                        "Har kuni yangi repo ochish portfolio emas. Bir nechta chuqurroq loyiha tanlang: auth, CRUD, API integration, dashboard yoki reporting kabi real use-caselarga ega bo'lsin. Ish beruvchi uchun 'bu odam product elementlarini tushunadimi?' degan savol muhimroq.",
                        "Bir loyiha ichida kod sifati, strukturasi, README va ishlash holati bor bo'lsa, u bir nechta random toy projectdan ancha yaxshi ko'rinadi. Sifat ustuvor.",
                    ],
                },
                {
                    "heading": "2. README - loyihaning sotuv matni",
                    "paragraphs": [
                        "Yaxshi README ko'p narsani hal qiladi. Qanday muammo yechilgan, qaysi texnologiyalar ishlatilgan, qanday ishga tushiriladi va qaysi qarorlar nima uchun tanlangan - bularni yozing. Bu sizning product thinking'ingizni ko'rsatadi.",
                        "Repo ichida kod yaxshi bo'lsa ham, izoh bo'lmasa ko'p narsa ko'rinmay qoladi. README - siz o'zingizni qanday taqdim etishingizning eng oson yo'li.",
                    ],
                },
                {
                    "heading": "3. Real use-case tanlang",
                    "paragraphs": [
                        "Portfolio loyihalari real hayotdagi muammoga yaqin bo'lsa, ta'siri oshadi. Masalan, course platform, task manager, analytics dashboard yoki booking flow kabi mahsulotlar. Chunki ular user, data va business logicni birlashtiradi.",
                        "Faqat tutorialni ko'chirish o'rniga, unga o'zingizdan biror feature qo'shing. Masalan admin analytics, search, role-based access yoki export. Shu nuqta sizning mustaqil fikrlaganingizni ko'rsatadi.",
                    ],
                },
                {
                    "heading": "4. Demo va deployment bo'lsa, yutuq ikki baravar",
                    "paragraphs": [
                        "Ishlaydigan demo mavjud bo'lsa, ishonch birdan oshadi. Repo borligi yaxshi, deploy bo'lgan versiya esa undan ham kuchli. Bu sizning kodni ishlabgina qolmay, yakunlashni ham bilishingizni ko'rsatadi.",
                        "Agar to'liq production deploy bo'lmasa ham, screenshotlar, video demo yoki qisqa walkthrough yozib qo'ying. Muhimi, loyiha 'tirik' ko'rinsin.",
                    ],
                },
            ],
            "Tajriba yo'qligi portfolioni zaif qilmaydi. Chuqurroq va real use-caselarga ega loyihalar, yaxshi README va imkon qadar demo sizni juda yaxshi ko'rsatadi. Portfolio - bu sizning amaliy kapitalingiz. Uni erta va ongli ravishda yig'ishni boshlang.",
        ),
    },
    {
        "title": "Uzbekistonda Python va Django bozorini qanday tushunish kerak?",
        "slug": "uzbekistonda-python-va-django-bozori",
        "excerpt": "Python va Django bozorini tushunish uchun vakansiyalar, product turi va talab qilinadigan yordamchi skilllarga qarash kerak.",
        "cover_image": UNSPLASH["team"],
        "topic": "Market Insight",
        "reading_time": 6,
        "seo_title": "Python course Uzbekistan va Django bozori haqida real qarash",
        "seo_description": "Uzbekistonda Python va Django bozorining qaysi skilllarga talab qilayotgani va juniorlar nimaga e'tibor berishi kerakligi haqida tahlil.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["Python course Uzbekistan", "Django bozori", "backend course tashkent"]),
        "published_at": date(2026, 1, 12),
        "featured": False,
        "content": build_article_html(
            "Uzbekistonda Python va Django bozorini qanday tushunish kerak?",
            "Python va Django'ga talab bormi? Bu savolni deyarli har bir boshlovchi beradi. To'g'ri javob shuki: talab bor, lekin u faqat framework nomi bilan belgilanmaydi. Bozor product turi, jamoa ehtiyoji va developerning qo'shimcha skilllari bilan shakllanadi. Shu sabab vakansiyani faqat 'Django bor yoki yo'q' degan filtr bilan o'qish yetarli emas.",
            [
                {
                    "heading": "1. Pythonning kuchi ko'p yo'nalishli ekanida",
                    "paragraphs": [
                        "Python backenddan tashqari automation, data va AI yo'nalishlarida ham ishlatiladi. Bu esa boshlovchi uchun katta afzallik: bir skill bir nechta bozorga chiqish imkonini beradi. Ammo aynan web productlar kontekstida Django hali ham juda amaliy tanlov bo'lib qolmoqda.",
                        "Kichik va o'rta bizneslar tezroq product chiqarishni xohlagani uchun Django'ning tayyor ekotizimi ko'p joyda foydali. Admin panel, auth, ORM va tez development - bu bozor ehtiyojiga mos keladi.",
                    ],
                },
                {
                    "heading": "2. Vakansiyalar framework emas, yechim qidiradi",
                    "paragraphs": [
                        "Ish beruvchi ko'pincha 'bizga Django biladigan odam' demaydi. U aslida 'bizga API yozadigan, database tushunadigan, deploy va debuggingdan qo'rqmaydigan odam' qidiradi. Framework bu yechimning bir qismi xolos.",
                        "Shu sabab Python/Django bilan birga REST API, SQL, Git va basic DevOps skilllar bo'lsa, siz ancha kuchli ko'rinasiz. Bozor aynan shu kombinatsiyani qadrlaydi.",
                    ],
                },
                {
                    "heading": "3. Tashkent va remote bozor uchun signal nima?",
                    "paragraphs": [
                        "Mahalliy bozor uchun portfolio va amaliy loyihalar juda kuchli signal. Remote uchun esa documentation reading, written communication va code quality yanada muhimlashadi. Ikkala holatda ham GitHub va aniq deliverable'lar foyda beradi.",
                        "Demak, faqat kursni tugatish bilan cheklanib qolmang. Amaliy projectlar, deploy va blog yozish ham sizni bozorga yaqinlashtiradi.",
                    ],
                },
                {
                    "heading": "4. Xulosa: bozorga skill stack bilan chiqing",
                    "paragraphs": [
                        "Python va Django bozoriga kirish uchun o'zingizni faqat bitta framework bilan cheklamang. Python fundamentals, Django, API, SQL va basic deploymentni qo'shib boring. Shu stack sizni nafaqat mahalliy, balki xalqaro ishlar uchun ham tayyorlaydi.",
                        "Bozorni tushunishning eng yaxshi usuli - vakansiya matnidagi ehtiyojlarni skill plan bilan bog'lash. Shunda o'qish jarayoni ancha strategik tus oladi.",
                    ],
                },
            ],
            "Uzbekistonda Python va Django uchun imkoniyat bor, ayniqsa siz frameworkdan tashqari productga kerak bo'ladigan yordamchi skilllarni ham rivojlantirsangiz. Backend course Tashkent yoki Django course online qidirayotganlar uchun eng yaxshi strategiya - bozorga mos skill stack yig'ishdir.",
        ),
    },
    {
        "title": "Backend engineerlar uchun DevOps basics: nimadan boshlash kerak?",
        "slug": "backend-engineerlar-uchun-devops-basics",
        "excerpt": "Deploy, Docker va monitoringdan qo'rqmaslik uchun backend engineerlar DevOps asoslarini erta o'rganishi kerak.",
        "cover_image": UNSPLASH["devops"],
        "topic": "DevOps",
        "reading_time": 6,
        "seo_title": "Backend engineerlar uchun DevOps basics",
        "seo_description": "Backend developerlar uchun Docker, CI/CD, environment variables va monitoringdan boshlanadigan DevOps asoslari.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["DevOps basics", "backend engineer", "Docker django"]),
        "published_at": date(2026, 1, 5),
        "featured": False,
        "content": build_article_html(
            "Backend engineerlar uchun DevOps basics: nimadan boshlash kerak?",
            "Backend engineer uchun deploy jarayonidan qo'rqmaslik juda katta ustunlik. Ko'pincha junior developer kod yozishni o'rganadi, lekin uning productionga qanday chiqishini tushunmaydi. Natijada ilova ishlasa ham, release paytida noaniqlik paydo bo'ladi. DevOps basics aynan shu bo'shliqni yopadi va operational confidence beradi.",
            [
                {
                    "heading": "1. Docker - muhit farqlarini kamaytirish vositasi",
                    "paragraphs": [
                        "Dockerning eng katta foydasi - 'menda ishladi' muammosini kamaytirish. Dependencies, Python versiyasi va servislar bir konteyner ichida aniq ko'rsatiladi. Bu team collaborationni ancha yengillashtiradi.",
                        "Backend engineer uchun Docker'ni chuqur orkestratsiya darajasida bilish shart emas. Lekin image build, run, env variables va compose kabi tushunchalarni bilish juda foydali.",
                    ],
                },
                {
                    "heading": "2. CI/CD - ishonchli release odati",
                    "paragraphs": [
                        "CI/CD faqat avtomatlashtirish emas, jamoa intizomining bir ko'rinishi. Testlar, lint, build va deploy bosqichlari aniqlashgan bo'lsa, relizlar xavfsizroq bo'ladi. Backend engineer uchun bu jarayonni tushunish product deliveryga yaqinlashtiradi.",
                        "GitHub Actions kabi vositalar bilan oddiy pipeline ham katta foyda beradi. Muhimi, pushdan releasegacha bo'lgan yo'l ko'rinadigan bo'lsin.",
                    ],
                },
                {
                    "heading": "3. Logs va monitoring - muammolarni tez topish kaliti",
                    "paragraphs": [
                        "Productiondagi muammoni local'da takrorlash har doim oson emas. Shu sabab logs va monitoring asoslari backend engineer uchun muhim. Qayerda xato berdi, qaysi endpoint sekin, qaysi servis javob bermayapti - buning barchasi kuzatuv bilan bilinadi.",
                        "Agar siz log yozishni va uni o'qishni bilsangiz, incident paytida ko'proq foyda bera olasiz. Bu esa jamoa ichida ishonchni oshiradi.",
                    ],
                },
                {
                    "heading": "4. Xavfsiz release mindsetini shakllantiring",
                    "paragraphs": [
                        "Release qilish - kodni serverga tashlab qo'yish emas. Environment variables, migrations, rollbacks, health checks va smoke testing haqida o'ylash kerak. Shu odat erta shakllansa, keyinchalik production bilan ishlash ancha osonlashadi.",
                        "DevOps basicsning maqsadi sizni to'liq infra engineer qilish emas, balki productni oxirigacha tushunadigan muhandisga aylantirishdir.",
                    ],
                },
            ],
            "Backend engineer uchun DevOps basics katta leverage beradi. Docker, CI/CD, logs va safe release odatlari sizni kuchliroq va ishonchliroq mutaxassis qiladi. Shu sabab bu mavzuni 'keyinroq'ga qoldirmaslik kerak.",
        ),
    },
    {
        "title": "Startuplar uchun monolith va microservices: qaysi biri to'g'ri qaror?",
        "slug": "startuplar-uchun-monolith-vs-microservices",
        "excerpt": "Erta bosqichdagi productlar uchun ko'pincha monolith tezroq va arzonroq. Microservices esa aniq ehtiyoj bo'lsa foyda beradi.",
        "cover_image": UNSPLASH["backend"],
        "topic": "Architecture",
        "reading_time": 7,
        "seo_title": "Monolith vs microservices for startups",
        "seo_description": "Startup productlarda monolith va microservices o'rtasidagi tanlovni delivery tezligi, jamoa hajmi va complexity asosida tahlil qilamiz.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["monolith vs microservices", "startup architecture", "backend architecture"]),
        "published_at": date(2025, 12, 28),
        "featured": False,
        "content": build_article_html(
            "Startuplar uchun monolith va microservices: qaysi biri to'g'ri qaror?",
            "Microservices haqida ko'p gapiriladi va ular ko'pincha 'katta' engineering darajasi sifatida ko'rsatiladi. Shu sabab yangi jamoalar ba'zan juda erta bu yo'nalishga o'tishga harakat qiladi. Ammo startup kontekstida eng muhim narsa - tez learning loop va kamroq operational murakkablik. Ko'p hollarda monolith aynan shu maqsadga xizmat qiladi.",
            [
                {
                    "heading": "1. Monolithning kuchi - fokus va tezlik",
                    "paragraphs": [
                        "Monolith bir kod bazasida ishlash, deploy va debuggingni soddalashtiradi. Kichik jamoa uchun bu juda katta afzallik, chunki kontekst bo'linmaydi. Feature chiqarish tezlashadi va decision-making arzonlashadi.",
                        "Ayniqsa product-market fit izlayotgan startupda bu juda muhim. Sizga ko'proq experiment qilish, kamroq operational overhead kerak bo'ladi. Monolith aynan shuni beradi.",
                    ],
                },
                {
                    "heading": "2. Microservices qachon mantiqli bo'ladi?",
                    "paragraphs": [
                        "Agar sizda alohida-scale bo'ladigan domainlar, mustaqil jamoalar yoki texnik cheklovlar bo'lsa, microservices foydali bo'lishi mumkin. Masalan, analytics pipeline yoki video processing servislar alohida yurishi kerak bo'lishi mumkin.",
                        "Lekin bu qaror faqat moda bo'lgani uchun qilinmasligi kerak. Microservices bilan infra, monitoring, tracing, contracts va deploylar ham ko'payadi. Bu esa kichik jamoa uchun qimmatga tushadi.",
                    ],
                },
                {
                    "heading": "3. Monolithni to'g'ri yozsangiz, uzoq yuradi",
                    "paragraphs": [
                        "Monolith yomon bo'lishi shart emas. Agar modul chegaralari, service layer va ownership aniq bo'lsa, u juda uzoq vaqt samarali ishlaydi. Ko'plab katta productlar ham bir necha yil yaxshi yozilgan monolith bilan o'sgan.",
                        "Muammo monolithning o'zida emas, tartibsiz kod bazasida. Shuning uchun avval architecture hygienega e'tibor bering.",
                    ],
                },
                {
                    "heading": "4. Qarorni business stage belgilaydi",
                    "paragraphs": [
                        "Startupning bosqichi, jamoa hajmi va product murakkabligi architecture tanlovini belgilashi kerak. Erta bosqichda tezlik va learning muhim bo'lsa, monolith kuchliroq. Aniq scale bottleneck va team independence kerak bo'lsa, microservices ustun bo'lishi mumkin.",
                        "Demak, 'katta kompaniyalar shunday qiladi' degan fikr bilan emas, o'zingizning product stage'ingiz bilan qaror qiling.",
                    ],
                },
            ],
            "Startuplar uchun architecture tanlovi texnik prestij masalasi emas. Bu business leverage masalasi. Ko'p hollarda yaxshi yozilgan monolith eng to'g'ri qaror bo'ladi. Microservices esa aniq ehtiyoj va tayyorlik bo'lganda kuchli vositaga aylanadi.",
        ),
    },
    {
        "title": "Python backend interview'ga qanday tayyorlanish kerak?",
        "slug": "python-backend-interviewga-qanday-tayyorlanish-kerak",
        "excerpt": "Interview tayyorgarligi theory yodlash emas, project explanation, basics va communicationni birga mashq qilishdir.",
        "cover_image": UNSPLASH["mentor"],
        "topic": "Interview",
        "reading_time": 6,
        "seo_title": "Python backend interview preparation guide",
        "seo_description": "Python backend interview uchun fundamentals, project explanation va coding communication bo'yicha amaliy tayyorgarlik reja.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["python backend interview", "django interview", "backend preparation"]),
        "published_at": date(2025, 12, 20),
        "featured": False,
        "content": build_article_html(
            "Python backend interview'ga qanday tayyorlanish kerak?",
            "Interview ko'pchilikka stressli ko'rinadi, ayniqsa birinchi ish uchun topshirayotganlar uchun. Odamlar ko'pincha juda ko'p theory yodlashga harakat qiladi, lekin interview jarayoni bundan kengroq. Sizning fikrlashingiz, projectlaringizni tushuntira olishingiz va asosiy conceptlarni to'g'ri ulay olishingiz muhim. Tayyorlanish ham aynan shunga mos bo'lishi kerak.",
            [
                {
                    "heading": "1. Fundamentalsni qayta ko'rib chiqing",
                    "paragraphs": [
                        "Python syntax, functions, OOP basics, lists vs tuples, dict usage, exceptions va context managers kabi mavzularni mustahkamlang. Backend uchun HTTP methods, status codes, auth va database basics ham ko'rilishi kerak. Interviewda ko'pincha murakkab savollar emas, aniq tushuncha tekshiriladi.",
                        "Agar siz fundamentallarni o'z projectlaringiz bilan bog'lay olsangiz, javoblaringiz ishonchliroq eshitiladi. Yodlangan gaplar esa tez bilinadi.",
                    ],
                },
                {
                    "heading": "2. Portfolio loyihalaringizni gapirib berishni mashq qiling",
                    "paragraphs": [
                        "Interviewer sizning qilgan ishingizni qanday tushuntirishingizga juda katta e'tibor beradi. Qaysi muammoni hal qildingiz, nima uchun aynan shu stackni tanladingiz, qaysi qiyinchilik bo'ldi va uni qanday hal qildingiz - shu savollarga tayyor bo'ling.",
                        "Bu javoblar theory savollaridan ham kuchliroq signal beradi. Chunki ular sizning real experience va ownership hissangizni ko'rsatadi.",
                    ],
                },
                {
                    "heading": "3. Ovoz chiqarib fikrlashni o'rganing",
                    "paragraphs": [
                        "Coding savolida jim qolish eng katta xatolardan biri. Siz mukammal javob topmaganingizda ham, qanday o'ylayotganingizni ayting. Trade-off, assumptions va possible approachlarni gapirib boring. Bu seniorlar uchun ham muhim ko'nikma.",
                        "Backend engineerning qadri ko'pincha muammoni qanday tahlil qilishida bilinadi. Communication bu yerda texnik skillning bir qismi.",
                    ],
                },
                {
                    "heading": "4. Mock interview va reflection qiling",
                    "paragraphs": [
                        "Biror do'st, mentor yoki kamera bilan mock interview qiling. Keyin o'zingizni tahlil qiling: qayerda to'xtalib qoldingiz, qaysi savolda ishonch past bo'ldi, nimani haddan tashqari cho'zib yubordingiz. Shu usul tayyorgarlikni tezlashtiradi.",
                        "Interview o'zi ham skill. Uni faqat bilim bilan emas, mashq bilan yaxshilash mumkin.",
                    ],
                },
            ],
            "Python backend interview'ga tayyorlanishda theory, project explanation va communicationni birga olib boring. Fundamentalsni mustahkamlang, loyihalaringizni hikoya qilib bera oling va mock interviewlar orqali o'zingizni sinab ko'ring. Shunda suhbatda ancha xotirjam va ishonchli bo'lasiz.",
        ),
    },
    {
        "title": "Junior developer uchun freelance yoki full-time: qaysi yo'l foydaliroq?",
        "slug": "junior-uchun-freelance-yoki-full-time",
        "excerpt": "Freelance ham, full-time ham foydali bo'lishi mumkin, lekin junior bosqichda o'sish tezligi va feedback muhimroq mezon bo'ladi.",
        "cover_image": UNSPLASH["team"],
        "topic": "Career Strategy",
        "reading_time": 6,
        "seo_title": "Freelance vs full-time for junior developers",
        "seo_description": "Junior developer uchun freelance va full-time yo'llarining afzalliklari, risklari va qaysi holatda qaysi biri foydaliroq ekanini tahlil qilamiz.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["freelance vs full-time", "junior developer career", "developer growth"]),
        "published_at": date(2025, 12, 13),
        "featured": False,
        "content": build_article_html(
            "Junior developer uchun freelance yoki full-time: qaysi yo'l foydaliroq?",
            "Developer bo'lishni boshlagan odam uchun bir payt savol paydo bo'ladi: men freelance ishlaymi yoki full-time kompaniyaga kiraymi? Har ikki yo'lning kuchli va zaif tomonlari bor. Lekin junior bosqichda asosiy mezon daromad emas, o'sish tezligi bo'lishi kerak. Chunki birinchi 1-2 yil davomida yig'ilgan odatlar va feedback keyingi karyeraga juda katta ta'sir qiladi.",
            [
                {
                    "heading": "1. Full-time ish structured growth beradi",
                    "paragraphs": [
                        "Kompaniya ichida siz code review, team workflow, deadlines va product contextni ko'rasiz. Bu ayniqsa junior uchun juda foydali. Chunki mustaqil ishlaganda ko'rinmaydigan ko'plab engineering odatlar jamoa ichida shakllanadi.",
                        "Shuningdek, real product ichida ishlash sizga priority, trade-off va ownershipni o'rgatadi. Bu skilllarni yolg'iz o'rganish qiyinroq.",
                    ],
                },
                {
                    "heading": "2. Freelance tezroq pul berishi mumkin, lekin feedback kamroq",
                    "paragraphs": [
                        "Freelance'da tezda kichik loyihalar olib, daromad ko'rish mumkin. Bu motivatsiya uchun foydali. Lekin ko'p mijozlar sizga mentorlash bermaydi. Ular natija kutadi. Junior esa aynan feedbackga ko'proq muhtoj bo'ladi.",
                        "Agar freelance qilmoqchi bo'lsangiz, kamida bitta mentor yoki kuchli community bo'lsin. Aks holda noto'g'ri odatlar mustahkamlanishi mumkin.",
                    ],
                },
                {
                    "heading": "3. Hybrid yondashuv ham ishlaydi",
                    "paragraphs": [
                        "Ko'pchilik uchun eng yaxshi variant - full-time yoki internship orqali foundation yig'ib, keyin asta-sekin freelance tasklar olish. Bu model bir vaqtning o'zida strukturali o'sish va mustaqil tajriba beradi.",
                        "Muhimi, freelance'ni faqat pul uchun emas, portfolio va client communication skill uchun ham ishlatish kerak. Shunda u career assetga aylanadi.",
                    ],
                },
                {
                    "heading": "4. Qarorni hozirgi ehtiyojingizga qarab qiling",
                    "paragraphs": [
                        "Agar sizga hozir feedback, jamoa va real product tajribasi kerak bo'lsa, full-time kuchliroq. Agar sizda allaqachon foundation bo'lsa va mustaqil ishlashga tayyor bo'lsangiz, freelance foydali bo'lishi mumkin.",
                        "Eng muhimi - qaysi yo'l sizni tezroq kuchli developerga aylantirishini o'ylang. Qisqa muddatli pul ko'pincha uzoq muddatli o'sishni almashtira olmaydi.",
                    ],
                },
            ],
            "Junior developer uchun ideal yo'l har doim ham bitta emas. Lekin boshlanishida feedback, team process va real product tajribasi ko'proq ahamiyatga ega. Shuning uchun full-time ko'p hollarda tezroq o'stiradi, freelance esa keyinroq yaxshi multiplikator bo'la oladi.",
        ),
    },
    {
        "title": "Git va GitHub workflow: jamoada professional ishlash uchun minimum standart",
        "slug": "git-va-github-workflow-jamoa-uchun",
        "excerpt": "Commit message, branch naming va pull request odatlari developerning professional darajasini ko'rsatadi.",
        "cover_image": UNSPLASH["workspace"],
        "topic": "Team Workflow",
        "reading_time": 6,
        "seo_title": "Git va GitHub workflow | Professional jamoa uchun minimum standart",
        "seo_description": "Git va GitHub bilan branch, commit, pull request va review odatlarini professional darajada yo'lga qo'yish bo'yicha qo'llanma.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["Git workflow", "GitHub workflow", "team collaboration"]),
        "published_at": date(2025, 12, 7),
        "featured": False,
        "content": build_article_html(
            "Git va GitHub workflow: jamoada professional ishlash uchun minimum standart",
            "Git bilish faqat commit qilishni bilish degani emas. Haqiqiy jamoa ishida branch naming, pull request sifati, reviewga tayyorlik va conflict bilan ishlash odatlari katta farq yaratadi. Ayniqsa junior developer uchun bu jihatlar professional signal beradi. Chunki jamoa sizning kod yozishingiz bilan birga, qanday ishlashingizni ham ko'radi.",
            [
                {
                    "heading": "1. Branch va commit naming beparvo bo'lmasin",
                    "paragraphs": [
                        "'fix', 'update', 'last-final-real' kabi nomlar jamoa uchun foydasiz. Branch nomi taskni anglatishi, commit esa o'zgarish niyatini ko'rsatishi kerak. Bu ko'rinishda mayda detal bo'lsa ham, long-term maintainability uchun juda muhim.",
                        "Yaxshi commit tarixini o'qib, feature qanday evolyutsiya qilganini tushunish mumkin. Yomon tarix esa chalkashlik yaratadi va debuggingni qiyinlashtiradi.",
                    ],
                },
                {
                    "heading": "2. Pull request - bu suhbat, zip fayl emas",
                    "paragraphs": [
                        "PR ochishdan maqsad faqat kodni merge qilish emas. Bu qarorlarni tushuntirish, risklarni ko'rsatish va reviewerni tezroq kontekstga kiritish imkonidir. Description yozing, screenshot qo'shing, qanday tekshirish mumkinligini yozing.",
                        "Shunda review tezlashadi va siz haqingizda 'fikrlab ishlaydi' degan taassurot paydo bo'ladi. Professionalizm shunaqa mayda nuqtalarda ko'rinadi.",
                    ],
                },
                {
                    "heading": "3. Review feedback'ni himoya sifatida emas, o'sish vositasi sifatida qabul qiling",
                    "paragraphs": [
                        "Ko'p juniorlar code review'ni tanqid deb qabul qiladi. Aslida esa bu jamoaviy sifat nazorati. Savol bering, fikrni tushuning va kerak bo'lsa trade-offni muhokama qiling. Bu jarayon sizni tez o'stiradi.",
                        "Review culture'ni to'g'ri qabul qilgan developerlar ancha tez professional darajaga chiqadi. Chunki ular feedbackdan qochmaydi.",
                    ],
                },
                {
                    "heading": "4. Conflict va rebase'dan qo'rqmang",
                    "paragraphs": [
                        "Jamoada ishlaganda conflict normal holat. Muhimi, undan qo'rqmaslik va tizimli hal qila bilish. Branchni yangilab turish, commitlarni tartibli ushlash va kichik PRlar qilish bu muammoni ancha kamaytiradi.",
                        "Git workflow'ni yaxshi bilish sizning jamoa ichidagi ish qulayligingizni oshiradi. Bu ko'nikma texnik skill bilan teng darajada foydali.",
                    ],
                },
            ],
            "Git va GitHub workflow - bu developerning professionallik ko'zgusi. Toza commitlar, aniq PR description va reviewga ochiq yondashuv sizni jamoa uchun ancha qulay mutaxassisga aylantiradi. Bu skillni erta shakllantirish katta yutuq beradi.",
        ),
    },
    {
        "title": "Backend developerlar uchun AI vositalari: 2026-yilda unumdorlikni qanday oshirish mumkin?",
        "slug": "backend-developerlar-uchun-ai-vositalari-2026",
        "excerpt": "AI vositalari kodni almashtirmaydi, lekin research, debugging va draft generation jarayonlarini sezilarli tezlashtiradi.",
        "cover_image": UNSPLASH["learning"],
        "topic": "AI Productivity",
        "reading_time": 6,
        "seo_title": "Backend developerlar uchun AI vositalari 2026",
        "seo_description": "AI vositalari backend developerlar uchun qayerda foydali, qayerda xavfli va ularni qanday ongli ishlatish kerakligi haqida amaliy qarash.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["AI tools for developers", "backend productivity", "developer workflow 2026"]),
        "published_at": date(2025, 11, 30),
        "featured": False,
        "content": build_article_html(
            "Backend developerlar uchun AI vositalari: 2026-yilda unumdorlikni qanday oshirish mumkin?",
            "AI vositalari atrofida shovqin ko'p, lekin backend developer uchun real foyda qayerda ekanini sovuqqonlik bilan ko'rish kerak. Ular tajribani almashtirmaydi, architecture qarorini sizning o'rningizga qabul qilmaydi. Ammo to'g'ri ishlatilsa, research, boilerplate drafting, debugging va documentation yozishda katta tezlik beradi. Muhimi - AI'ni tayyor javob manbai emas, fikrlashni tezlashtiruvchi vosita sifatida ko'rish.",
            [
                {
                    "heading": "1. Boilerplate va draftlar uchun juda foydali",
                    "paragraphs": [
                        "Serializer skeleton, test case draft, docstring yoki README outline kabi ishlarda AI yaxshi yordam beradi. Bu sizni zero-to-one bosqichida tezlashtiradi. Ayniqsa charchagan paytda blank page effektini kamaytiradi.",
                        "Lekin draftni kritik ko'z bilan ko'rib chiqish shart. Naming, edge case va business logicni baribir developer hal qiladi.",
                    ],
                },
                {
                    "heading": "2. Debuggingda ikkinchi fikr sifatida ishlating",
                    "paragraphs": [
                        "Error message, stack trace yoki g'alati query resultni AI bilan birga tahlil qilish foydali bo'lishi mumkin. U siz ko'rmayotgan ehtimoliy sabablarni ko'rsatadi. Bu ayniqsa o'rganish jarayonida samarali.",
                        "Ammo ko'r-ko'rona ishonish xavfli. AI ba'zan ishonchli ohangda noto'g'ri maslahat beradi. Shu sabab uning javoblarini documentation va o'z logikangiz bilan tekshirish kerak.",
                    ],
                },
                {
                    "heading": "3. Architecture va securityda ehtiyot bo'ling",
                    "paragraphs": [
                        "AI ko'pincha umumiy tavsiya beradi. Lekin sizning product, trafik, data sensitivity va jamoa kontekstingizni to'liq bilmaydi. Shu sabab architecture yoki security bilan bog'liq qarorlarni faqat AI javobiga tayab qabul qilish xavfli.",
                        "Bu sohalarda AI ko'proq brainstorming vositasi bo'lishi mumkin, yakuniy qaror beruvchi emas.",
                    ],
                },
                {
                    "heading": "4. Eng yaxshi natija - kuchli muhandis + kuchli vosita",
                    "paragraphs": [
                        "AI eng ko'p foyda bergan holat shuki, asosiy fundamentals mustahkam bo'lsa. Shunda siz savolni to'g'ri bera olasiz, javobni filtrlaysiz va natijani tez integratsiya qilasiz. Zaif foundation bilan esa u chalg'itishi mumkin.",
                        "Demak, AI productivity leverage beradi, lekin leverage bo'lishi uchun tayanch ham kerak. Tooldan oldin skill, skill ustiga tool.",
                    ],
                },
            ],
            "AI vositalari backend developerning o'rnini bosmaydi, lekin to'g'ri ishlatilsa, unumdorlikni sezilarli oshiradi. Boilerplate, research va debuggingda ulardan foydalaning, ammo architecture, security va business-critical qarorlarda mustaqil fikrni saqlang. Eng yaxshi kombinatsiya - kuchli foundation va ongli tool usage.",
        ),
    },
    {
        "title": "Dasturchilar uchun chuqur ishlash: ko'proq vaqt emas, ko'proq fokus qanday beradi?",
        "slug": "dasturchilar-uchun-chuqur-ishlash",
        "excerpt": "Ko'p ishlash va ko'p natija bir xil narsa emas. Dasturchi uchun fokusli bloklar ko'pincha uzun ish soatlaridan kuchliroq.",
        "cover_image": UNSPLASH["workspace"],
        "topic": "Productivity",
        "reading_time": 6,
        "seo_title": "Dasturchilar uchun deep work: ko'proq fokus qanday beradi?",
        "seo_description": "Developerlar uchun deep work tamoyillari: fokus bloklari, chalg'ituvchilarni kamaytirish va amaliy coding outputni oshirish usullari.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["deep work for developers", "developer productivity", "focus for coding"]),
        "published_at": date(2025, 11, 23),
        "featured": False,
        "content": build_article_html(
            "Dasturchilar uchun chuqur ishlash: ko'proq vaqt emas, ko'proq fokus qanday beradi?",
            "Ko'p boshlovchilar yaxshi developer bo'lish uchun kuniga 10-12 soat ishlash kerak deb o'ylaydi. Amalda esa katta farqni ish soati emas, fokus sifati beradi. Dasturchining eng kuchli resursi - toza fikrlash. Agar bu resurs doimiy bo'linib tursa, hatto uzoq vaqt o'tirgan bo'lsangiz ham, natija past bo'lishi mumkin. Deep work shu nuqtada juda foydali yondashuv.",
            [
                {
                    "heading": "1. Context switching - yashirin energiya yo'qotish",
                    "paragraphs": [
                        "Bir taskdan boshqasiga sakrash miyaning katta energiyasini oladi. Slack, Telegram, brauzer tablari va random videolar kod oqimini bo'lib yuboradi. Natijada murakkab mantiqiy muammoni tutib turish qiyinlashadi.",
                        "Backend yoki debugging kabi ishlar ayniqsa uzluksiz diqqat talab qiladi. Shu sabab chalg'ituvchilarni minimallashtirish samarani ancha oshiradi.",
                    ],
                },
                {
                    "heading": "2. 60-90 daqiqalik fokus bloklari ishlaydi",
                    "paragraphs": [
                        "Ko'pchilik uchun 60-90 daqiqalik chuqur bloklar juda samarali. Shu vaqt ichida bitta aniq vazifani tanlang: feature, bugfix, article outline yoki refactor. Maqsadning aniq bo'lishi fokusni kuchaytiradi.",
                        "Blok oxirida qisqa review qiling: nima tugadi, nima qoldi. Bu keyingi sessiyani tez boshlashga yordam beradi.",
                    ],
                },
                {
                    "heading": "3. Fokusni marosimga aylantiring",
                    "paragraphs": [
                        "Har safar chuqur ish boshlashdan oldin bir xil tayyorgarlik qilsangiz, miya tezroq moslashadi. Masalan, telefonni olib qo'yish, kerakli tablardan boshqasini yopish, timer qo'yish va taskni yozib qo'yish. Bu mayda odatlar ritm yaratadi.",
                        "Dasturchilar uchun muhit dizayni ko'pincha motivatsiyadan ham kuchliroq ishlaydi. O'zingizga fokusni osonlashtiradigan sharoit yarating.",
                    ],
                },
                {
                    "heading": "4. Output bilan o'lchang",
                    "paragraphs": [
                        "Kun oxirida 'qancha o'tirdim?' degan savoldan ko'ra 'nima tugatdim?' muhimroq. Deep work tamoyili ham shuni ko'zlaydi. Sizni soatlar emas, yakunlangan deliverable oldinga siljitadi.",
                        "Developerning o'sishi ko'pincha muntazam, fokusli chiqishlarga bog'liq. Har kuni oz bo'lsa ham sifatli output uzun muddatda katta farq qiladi.",
                    ],
                },
            ],
            "Ko'proq ishlash har doim ko'proq natija bermaydi. Developer uchun chuqur va fokusli bloklar ancha kuchli leverage beradi. Chalg'ituvchilarni kamaytiring, aniq task tanlang va outputni kuzating. Shunda o'qish ham, ish ham tezroq oldinga siljiydi.",
        ),
    },
    {
        "title": "Backend developer uchun documentation o'qish odatini qanday shakllantirish mumkin?",
        "slug": "documentation-oqish-odatini-qanday-shakllantirish-mumkin",
        "excerpt": "Documentation o'qish sekinlik belgisi emas - bu mustaqil va kuchli developer bo'lishning asosiy odatlaridan biri.",
        "cover_image": UNSPLASH["notebook"],
        "topic": "Learning Skills",
        "reading_time": 6,
        "seo_title": "Documentation o'qish odati | Backend developer uchun muhim skill",
        "seo_description": "Backend developerlar uchun official documentationni samarali o'qish, filterlash va amalda qo'llash bo'yicha tavsiyalar.",
        "meta_keywords": ", ".join(GLOBAL_KEYWORDS + ["documentation reading", "backend learning", "django docs"]),
        "published_at": date(2025, 11, 16),
        "featured": False,
        "content": build_article_html(
            "Backend developer uchun documentation o'qish odatini qanday shakllantirish mumkin?",
            "Documentation o'qish ko'pchilikka qiyin va zerikarli ko'rinadi. Shu sabab odamlar ko'pincha faqat video yoki bloglarga tayanib qoladi. Lekin backend engineer uchun official docs bilan ishlash mustaqillikning asosiy belgilaridan biri. Documentation sizga faqat 'qanday'ni emas, ko'pincha 'nima uchun'ni ham beradi. Shu sabab bu odatni erta shakllantirish katta farq qiladi.",
            [
                {
                    "heading": "1. Documentationni boshidan oxirigacha o'qish shart emas",
                    "paragraphs": [
                        "Ko'p odam documentationni kitobdek o'qishga harakat qiladi va charchab qoladi. Aslida esa docs - reference vositasi. Sizga ayni paytda kerak bo'lgan qismini topish va uni amalda qo'llash muhimroq.",
                        "Masalan, DRF permissions yozayotgan bo'lsangiz, aynan shu bo'limni oching. Keyin related conceptlarni ko'rib chiqing. Kontekstli o'qish ancha samarali.",
                    ],
                },
                {
                    "heading": "2. Kod bilan birga o'qing",
                    "paragraphs": [
                        "Docsni faqat ko'z yugurtirib o'qishdan ko'ra, yonida editor ochiq turgani foydali. O'qigan misolni o'zingizda qayta yozing, kichik variantlar bilan sinab ko'ring. Shunda ma'lumot passiv emas, aktiv bilimga aylanadi.",
                        "Bu usul ayniqsa framework va kutubxonalar uchun juda yaxshi ishlaydi. Django yoki PostgreSQL docs shu tarzda ancha tez o'zlashtiriladi.",
                    ],
                },
                {
                    "heading": "3. Documentation savolga javob beruvchi vosita bo'lsin",
                    "paragraphs": [
                        "Agar savolsiz docsga kirsangiz, ko'p narsani ushlash qiyin bo'ladi. Avval savolni aniqlang: Nega bu query sekin? DRF permission qayerda tekshiriladi? Transaction qachon kerak? Shu savol docs o'qishni yo'naltiradi.",
                        "Yaxshi savol documentation bilan ishlash sifatini oshiradi. Seniorlar ko'pincha shu uchun docsni tezroq va samaraliroq o'qiydi.",
                    ],
                },
                {
                    "heading": "4. Shaxsiy note va summary yozing",
                    "paragraphs": [
                        "Muhim bo'limlarni o'qigach, o'zingizcha qisqa summary yozing. Bu xotirani mustahkamlaydi va keyin qaytishda tezlik beradi. Har safar bir mavzuni qayta nolдан boshlash shart bo'lmaydi.",
                        "Documentation bilan do'stlashgan developer mustaqilroq bo'ladi. U resurs yetishmasa ham yo'lini topa oladi.",
                    ],
                },
            ],
            "Documentation o'qish - sekinlik emas, professional mustaqillik. Uni context bilan, kod bilan va aniq savollar bilan o'qisangiz, jarayon ancha osonlashadi. Backend developer sifatida bu odat sizga butun karyera davomida xizmat qiladi.",
        ),
    },
]

_BOOTSTRAPPED = False


def get_language(request):
    lang = request.GET.get("lang", DEFAULT_LANGUAGE)
    return lang if lang in LANGUAGE_OPTIONS else DEFAULT_LANGUAGE


def translate_map(value, lang, fallback=DEFAULT_LANGUAGE):
    if isinstance(value, dict):
        return value.get(lang) or value.get(fallback) or next(iter(value.values()), "")
    return value


def with_lang(url, lang):
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}lang={lang}"


def global_keywords(extra=None):
    items = list(GLOBAL_KEYWORDS)
    if extra:
        items.extend(extra)
    return ", ".join(dict.fromkeys(items))


def annotate_category(category, lang):
    category.display_name = translate_map((category.translations or {}).get("name", {}), lang) or category.name
    category.display_description = translate_map((category.translations or {}).get("description", {}), lang) or category.description
    category.href = with_lang(reverse("centers_by_category", args=[category.slug]), lang)
    return category


def annotate_center(center, lang):
    center.display_name = center.name
    center.display_headline = translate_map((center.translations or {}).get("headline", {}), lang) or center.headline
    center.display_description = translate_map((center.translations or {}).get("description", {}), lang) or center.description
    center.feature_list = center.features or []
    center.href = with_lang(reverse("center_detail", args=[center.slug]), lang)
    center.category_names = [annotate_category(category, lang).display_name for category in center.categories.all()]
    return center


def annotate_course(course, lang):
    course.display_name = translate_map((course.translations or {}).get("name", {}), lang) or course.name
    course.display_subtitle = translate_map((course.translations or {}).get("subtitle", {}), lang) or course.subtitle
    course.display_description = translate_map((course.translations or {}).get("description", {}), lang) or course.description
    course.feature_list = course.highlights or []
    course.outcome_list = course.outcomes or []
    course.curriculum_list = course.curriculum or []
    course.href = with_lang(reverse("course_detail", args=[course.slug]), lang)
    course.enroll_href = with_lang(reverse("enroll_course", args=[course.id]), lang)
    return course


def annotate_blog(blog, lang):
    blog.display_title = translate_map((blog.translations or {}).get("title", {}), lang) or blog.title
    blog.display_excerpt = translate_map((blog.translations or {}).get("excerpt", {}), lang) or blog.excerpt
    blog.href = with_lang(reverse("blog_detail", args=[blog.slug]), lang)
    return blog


def annotate_testimonial(testimonial, lang):
    testimonial.display_quote = translate_map((testimonial.translations or {}).get("quote", {}), lang) or testimonial.quote
    testimonial.display_role = translate_map((testimonial.translations or {}).get("role", {}), lang) or testimonial.role
    return testimonial


def build_structured_data(payload):
    return json.dumps(payload, ensure_ascii=False, indent=2)


def build_common_context(request, seo):
    lang = get_language(request)
    ui = UI_COPY[lang]
    home_url = with_lang(reverse("dashboard"), lang)
    blog_list_url = with_lang(reverse("blog_list"), lang)
    base_navigation = {
        "home": home_url,
        "courses": f"{home_url}#courses",
        "centers": f"{home_url}#centers",
        "blog": blog_list_url,
        "about": f"{home_url}#about",
        "contact": f"{home_url}#contact",
        "login": with_lang(reverse("login"), lang),
        "register": with_lang(reverse("register"), lang),
        "profile": with_lang(reverse("profile"), lang),
        "logout": with_lang(reverse("logout"), lang),
    }
    nav_menu = build_nav_menu(lang, base_navigation)
    languages = []
    current_path = request.path
    for code in LANGUAGE_OPTIONS:
        meta = LANGUAGE_META[code]
        languages.append({
            "code": code,
            "label": meta["label"],
            "short": meta["short"],
            "native": meta["native"],
            "flag_alt": meta["flag_alt"],
            "flag_svg": meta["flag_svg"],
            "url": with_lang(current_path, code),
            "is_current": code == lang,
        })
    current_language = next((item for item in languages if item["is_current"]), languages[0])
    return {
        "lang": lang,
        "lang_query": f"?lang={lang}",
        "language_options": {code: with_lang(current_path, code) for code in LANGUAGE_OPTIONS},
        "language_labels": LANGUAGE_OPTIONS,
        "languages": languages,
        "current_language": current_language,
        "ui": ui,
        "navigation": base_navigation,
        "nav_menu": nav_menu,
        "seo": seo,
        "site_name": ui["meta_site_name"],
        "sticky_primary_href": f"{home_url}#courses",
        "sticky_secondary_href": f"{home_url}#contact",
        "current_url": request.build_absolute_uri(),
        "home_url": home_url,
    }


def build_nav_menu(lang, navigation):
    blog_url = navigation["blog"]
    contact_url = navigation["contact"]
    about_url = navigation["about"]

    category_links = []
    try:
        categories = list(Category.objects.all())
    except Exception:
        categories = []
    for category in categories:
        annotated = annotate_category(category, lang)
        category_links.append({
            "label": annotated.display_name,
            "description": annotated.display_description,
            "href": annotated.href,
            "icon": annotated.icon,
        })

    course_links = []
    try:
        featured_courses = list(Course.objects.filter(featured=True).select_related("learning_center")[:4])
    except Exception:
        featured_courses = []
    for course in featured_courses:
        annotated = annotate_course(course, lang)
        course_links.append({
            "label": annotated.display_name,
            "description": annotated.display_subtitle,
            "href": annotated.href,
            "icon": "→",
        })

    if lang == "uz":
        labels = {
            "all_courses": "Barcha kurslar",
            "all_courses_desc": "Featured trekları va to'liq kurs katalogi",
            "all_centers": "Barcha markazlar",
            "all_centers_desc": "Web, Backend, Data va DevOps yo'nalishlari",
            "blog_topic_python": "Python roadmap",
            "blog_topic_python_desc": "Boshlovchidan junior backendgacha qadamlar",
            "blog_topic_django": "Django va REST API",
            "blog_topic_django_desc": "Architecture, auth va product workflow",
            "blog_topic_career": "Karyera va portfolio",
            "blog_topic_career_desc": "Junior backend ishga olishda nima muhim",
            "blog_all": "Barcha maqolalar",
            "blog_all_desc": "EduPlanet blog arxivi",
            "about_mentor": "Mentor sifatida",
            "about_mentor_desc": "Asilbek bilan o'qish formati va kutiladigan natijalar",
            "about_skills": "Tech stack",
            "about_skills_desc": "Python, Django, PostgreSQL, DevOps",
            "about_mission": "Mission va falsafa",
            "about_mission_desc": "Nega EduPlanet va kim uchun yaratilgan",
            "contact_book": "Konsultatsiyaga yozilish",
            "contact_book_desc": "Karyera yoki kurs tanlash bo'yicha 30 daqiqalik suhbat",
            "contact_email": "Email bilan yozish",
            "contact_email_desc": "asilbekmirolimov@gmail.com — 1 ish kuni ichida javob",
            "contact_telegram": "Telegram orqali",
            "contact_telegram_desc": "@mirolimov_a — tezkor savollar uchun",
        }
    elif lang == "en":
        labels = {
            "all_courses": "All courses",
            "all_courses_desc": "Featured tracks and the full catalog",
            "all_centers": "All centers",
            "all_centers_desc": "Web, Backend, Data, and DevOps tracks",
            "blog_topic_python": "Python roadmap",
            "blog_topic_python_desc": "From beginner to junior backend, step by step",
            "blog_topic_django": "Django & REST API",
            "blog_topic_django_desc": "Architecture, auth, and product workflow",
            "blog_topic_career": "Career & portfolio",
            "blog_topic_career_desc": "What hiring teams actually look for",
            "blog_all": "All articles",
            "blog_all_desc": "Browse the EduPlanet blog archive",
            "about_mentor": "As a mentor",
            "about_mentor_desc": "How learning with Asilbek works in practice",
            "about_skills": "Tech stack",
            "about_skills_desc": "Python, Django, PostgreSQL, DevOps",
            "about_mission": "Mission & philosophy",
            "about_mission_desc": "Why EduPlanet exists and who it serves",
            "contact_book": "Book a consultation",
            "contact_book_desc": "30-minute career or course-fit chat",
            "contact_email": "Email us",
            "contact_email_desc": "asilbekmirolimov@gmail.com — reply within one business day",
            "contact_telegram": "Telegram",
            "contact_telegram_desc": "@mirolimov_a for quick questions",
        }
    else:
        labels = {
            "all_courses": "Все курсы",
            "all_courses_desc": "Featured-треки и полный каталог",
            "all_centers": "Все направления",
            "all_centers_desc": "Web, Backend, Data и DevOps",
            "blog_topic_python": "Python roadmap",
            "blog_topic_python_desc": "От новичка до junior backend, шаг за шагом",
            "blog_topic_django": "Django и REST API",
            "blog_topic_django_desc": "Architecture, auth и product workflow",
            "blog_topic_career": "Карьера и портфолио",
            "blog_topic_career_desc": "Что реально ценят при найме",
            "blog_all": "Все статьи",
            "blog_all_desc": "Архив блога EduPlanet",
            "about_mentor": "Как наставник",
            "about_mentor_desc": "Как устроено обучение с Асилбеком",
            "about_skills": "Tech stack",
            "about_skills_desc": "Python, Django, PostgreSQL, DevOps",
            "about_mission": "Миссия и философия",
            "about_mission_desc": "Зачем EduPlanet и для кого",
            "contact_book": "Записаться на консультацию",
            "contact_book_desc": "30-минутный разговор по карьере или выбору курса",
            "contact_email": "Написать на email",
            "contact_email_desc": "asilbekmirolimov@gmail.com — ответ в течение рабочего дня",
            "contact_telegram": "Telegram",
            "contact_telegram_desc": "@mirolimov_a — быстрые вопросы",
        }

    courses_submenu = list(course_links)
    courses_submenu.append({
        "label": labels["all_courses"],
        "description": labels["all_courses_desc"],
        "href": navigation["courses"],
        "icon": "★",
    })

    centers_submenu = list(category_links)
    centers_submenu.append({
        "label": labels["all_centers"],
        "description": labels["all_centers_desc"],
        "href": navigation["centers"],
        "icon": "◎",
    })

    blog_submenu = [
        {"label": labels["blog_topic_python"], "description": labels["blog_topic_python_desc"], "href": blog_url, "icon": "Py"},
        {"label": labels["blog_topic_django"], "description": labels["blog_topic_django_desc"], "href": blog_url, "icon": "Dj"},
        {"label": labels["blog_topic_career"], "description": labels["blog_topic_career_desc"], "href": blog_url, "icon": "→"},
        {"label": labels["blog_all"], "description": labels["blog_all_desc"], "href": blog_url, "icon": "★"},
    ]

    about_submenu = [
        {"label": labels["about_mentor"], "description": labels["about_mentor_desc"], "href": about_url, "icon": "AM"},
        {"label": labels["about_skills"], "description": labels["about_skills_desc"], "href": about_url, "icon": "</>"},
        {"label": labels["about_mission"], "description": labels["about_mission_desc"], "href": about_url, "icon": "◎"},
    ]

    contact_submenu = [
        {"label": labels["contact_book"], "description": labels["contact_book_desc"], "href": contact_url, "icon": "✱"},
        {"label": labels["contact_email"], "description": labels["contact_email_desc"], "href": "mailto:asilbekmirolimov@gmail.com", "icon": "@"},
        {"label": labels["contact_telegram"], "description": labels["contact_telegram_desc"], "href": "https://t.me/mirolimov_a", "icon": "✈"},
    ]

    ui = UI_COPY[lang]
    return [
        {"key": "home", "label": ui["home"], "href": navigation["home"], "submenu": []},
        {"key": "courses", "label": ui["courses"], "href": navigation["courses"], "submenu": courses_submenu},
        {"key": "centers", "label": ui["centers"], "href": navigation["centers"], "submenu": centers_submenu},
        {"key": "blog", "label": ui["blog"], "href": navigation["blog"], "submenu": blog_submenu},
        {"key": "about", "label": ui["about"], "href": navigation["about"], "submenu": about_submenu},
        {"key": "contact", "label": ui["contact"], "href": navigation["contact"], "submenu": contact_submenu},
    ]


def ensure_platform_content(force=False):
    global _BOOTSTRAPPED
    if _BOOTSTRAPPED and not force:
        return

    User = get_user_model()

    with transaction.atomic():
        instructor_user, _ = User.objects.get_or_create(
            username=INSTRUCTOR_DATA["username"],
            defaults={
                "email": INSTRUCTOR_DATA["email"],
                "first_name": INSTRUCTOR_DATA["first_name"],
                "last_name": INSTRUCTOR_DATA["last_name"],
            },
        )
        for field in ["email", "first_name", "last_name"]:
            setattr(instructor_user, field, INSTRUCTOR_DATA[field])
        if not instructor_user.has_usable_password():
            instructor_user.set_password("Eduplanet!2026")
        instructor_user.save()

        InstructorProfile.objects.update_or_create(
            user=instructor_user,
            defaults={
                "title": INSTRUCTOR_DATA["title"],
                "bio": INSTRUCTOR_DATA["bio"],
                "mission": INSTRUCTOR_DATA["mission"],
                "profile_description": INSTRUCTOR_DATA["profile_description"],
                "experience_years": INSTRUCTOR_DATA["experience_years"],
                "skills": INSTRUCTOR_DATA["skills"],
                "location": INSTRUCTOR_DATA["location"],
                "website": INSTRUCTOR_DATA["website"],
                "linkedin": INSTRUCTOR_DATA["linkedin"],
                "github": INSTRUCTOR_DATA["github"],
                "telegram": INSTRUCTOR_DATA["telegram"],
                "avatar_url": INSTRUCTOR_DATA["avatar_url"],
                "translations": INSTRUCTOR_DATA["translations"],
            },
        )

        category_map = {}
        for item in CATEGORY_DATA:
            category, _ = Category.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "name": item["name"],
                    "description": item["description"],
                    "icon": item["icon"],
                    "translations": item["translations"],
                },
            )
            category_map[item["slug"]] = category
        Category.objects.exclude(slug__in=[item["slug"] for item in CATEGORY_DATA]).delete()

        center_map = {}
        for item in CENTER_DATA:
            center, _ = LearningCenter.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "name": item["name"],
                    "headline": item["headline"],
                    "description": item["description"],
                    "location": item["location"],
                    "email": item["email"],
                    "phone_number": item["phone_number"],
                    "image": item["image"],
                    "website": item["website"],
                    "students_count": item["students_count"],
                    "mentors_count": item["mentors_count"],
                    "courses_count": item["courses_count"],
                    "features": item["features"],
                    "translations": item["translations"],
                    "seo_title": f"{item['name']} | EduPlanet Learning Center",
                    "seo_description": item["description"][:160],
                    "meta_keywords": global_keywords([item["name"], "learning center", "online education"]),
                },
            )
            center.categories.set([category_map[slug] for slug in item["categories"]])
            center_map[item["slug"]] = center
        LearningCenter.objects.exclude(slug__in=[item["slug"] for item in CENTER_DATA]).delete()

        course_map = {}
        for item in COURSE_DATA:
            course, _ = Course.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "name": item["name"],
                    "subtitle": item["subtitle"],
                    "description": item["description"],
                    "learning_center": center_map[item["center"]],
                    "image": item["image"],
                    "level": item["level"],
                    "duration": item["duration"],
                    "lessons_count": item["lessons_count"],
                    "students_count": item["students_count"],
                    "hours_watched": item["hours_watched"],
                    "price": item["price"],
                    "rating": item["rating"],
                    "highlights": item["highlights"],
                    "outcomes": item["outcomes"],
                    "curriculum": item["curriculum"],
                    "translations": item["translations"],
                    "seo_title": item["seo_title"],
                    "seo_description": item["seo_description"],
                    "meta_keywords": item["meta_keywords"],
                    "featured": item["featured"],
                },
            )
            course_map[item["slug"]] = course
            existing_names = []
            for index, video in enumerate(item["videos"], start=1):
                name, description, url, cover, duration, preview = video
                existing_names.append(name)
                VideoContent.objects.update_or_create(
                    course=course,
                    name=name,
                    defaults={
                        "description": description,
                        "video_url": url,
                        "cover_image": cover,
                        "duration": duration,
                        "sort_order": index,
                        "is_preview": preview,
                    },
                )
            VideoContent.objects.filter(course=course).exclude(name__in=existing_names).delete()
        Course.objects.exclude(slug__in=[item["slug"] for item in COURSE_DATA]).delete()

        blog_slugs = []
        for item in BLOG_DATA:
            blog_slugs.append(item["slug"])
            blog, _ = BlogPost.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "excerpt": item["excerpt"],
                    "content": item["content"],
                    "author_name": "Asilbek Mirolimov",
                    "cover_image": item["cover_image"],
                    "reading_time": item["reading_time"],
                    "topic": item["topic"],
                    "seo_title": item["seo_title"],
                    "seo_description": item["seo_description"],
                    "meta_keywords": item["meta_keywords"],
                    "translations": {
                        "title": {"uz": item["title"], "en": item["title"], "ru": item["title"]},
                        "excerpt": {"uz": item["excerpt"], "en": item["excerpt"], "ru": item["excerpt"]},
                    },
                    "published_at": item["published_at"],
                    "featured": item["featured"],
                },
            )
            BlogImage.objects.update_or_create(blog_post=blog, image_url=item["cover_image"])
        BlogPost.objects.exclude(slug__in=blog_slugs).delete()

        testimonial_names = []
        for item in TESTIMONIAL_DATA:
            testimonial_names.append(item["name"])
            Testimonial.objects.update_or_create(
                name=item["name"],
                defaults={
                    "role": item["role"],
                    "quote": item["quote"],
                    "avatar_url": item["avatar_url"],
                    "rating": item["rating"],
                    "sort_order": item["sort_order"],
                    "translations": {
                        "quote": {"uz": item["quote"], "en": item["quote"], "ru": item["quote"]},
                        "role": {"uz": item["role"], "en": item["role"], "ru": item["role"]},
                    },
                },
            )
        Testimonial.objects.exclude(name__in=testimonial_names).delete()

        learner = User.objects.exclude(pk=instructor_user.pk).order_by("pk").first()
        if learner:
            for course in Course.objects.filter(featured=True)[:2]:
                UserCourse.objects.get_or_create(user=learner, course=course)

    _BOOTSTRAPPED = True


def get_instructor_profile(lang):
    profile = InstructorProfile.objects.select_related("user").first()
    if not profile:
        return None
    profile.display_title = translate_map((profile.translations or {}).get("title", {}), lang) or profile.title
    profile.display_bio = translate_map((profile.translations or {}).get("bio", {}), lang) or profile.bio
    profile.display_mission = translate_map((profile.translations or {}).get("mission", {}), lang) or profile.mission
    profile.display_profile_description = translate_map((profile.translations or {}).get("profile_description", {}), lang) or profile.profile_description
    return profile


def build_homepage_extras(lang, featured_courses, all_courses, centers, blogs):
    extras = HOME_EXTRAS[lang]
    course_map = {course.slug: course for course in all_courses}
    center_map = {center.slug: center for center in centers}
    hero_spotlights = []
    for index, course in enumerate(featured_courses[:3], start=1):
        hero_spotlights.append({
            "id": f"spotlight-{index}",
            "eyebrow": f"Track {index:02d}",
            "title": course.display_name,
            "description": course.display_subtitle,
            "image": course.image,
            "href": course.href,
            "stats": [
                {"label": UI_COPY[lang]["level_label"], "value": course.level},
                {"label": UI_COPY[lang]["duration_label"], "value": course.duration},
                {"label": UI_COPY[lang]["students_label"], "value": f"{course.students_count}+"},
            ],
            "center": course.learning_center.name if course.learning_center_id else "EduPlanet",
        })

    goal_paths = []
    for item in extras["goal_paths"]:
        course = course_map.get(item["course_slug"])
        center = center_map.get(item["center_slug"])
        goal_paths.append({
            **item,
            "course": course,
            "center": center,
        })

    return {
        "trust_strip": extras["trust_strip"],
        "momentum_label": extras["momentum_label"],
        "momentum_title": extras["momentum_title"],
        "momentum_description": extras["momentum_description"],
        "recent_activity": extras["recent_activity"],
        "platform_pillars": extras["platform_pillars"],
        "journey_label": extras["journey_label"],
        "journey_title": extras["journey_title"],
        "journey_description": extras["journey_description"],
        "journey_steps": extras["journey_steps"],
        "experience_label": extras["experience_label"],
        "experience_title": extras["experience_title"],
        "experience_description": extras["experience_description"],
        "experience_modes": extras["experience_modes"],
        "path_label": extras["path_label"],
        "path_title": extras["path_title"],
        "path_description": extras["path_description"],
        "path_primary": extras["path_primary"],
        "path_secondary": extras["path_secondary"],
        "goal_paths": goal_paths,
        "hero_spotlights": hero_spotlights,
        "featured_blog_spotlight": blogs[0] if blogs else None,
        "blog_spotlight_label": extras["blog_spotlight_label"],
    }


def get_homepage_context(request):
    ensure_platform_content()
    lang = get_language(request)
    all_courses = [annotate_course(course, lang) for course in Course.objects.select_related("learning_center").all()]
    courses = [course for course in all_courses if course.featured][:6]
    centers = [annotate_center(center, lang) for center in LearningCenter.objects.prefetch_related("categories")]
    categories = [annotate_category(category, lang) for category in Category.objects.all()]
    blogs = [annotate_blog(blog, lang) for blog in BlogPost.objects.filter(featured=True)[:4]]
    testimonials = [annotate_testimonial(item, lang) for item in Testimonial.objects.all()[:6]]
    instructor = get_instructor_profile(lang)
    total_students = max(sum(course.students_count for course in Course.objects.all()), 1200)
    total_hours = max(sum(course.hours_watched for course in Course.objects.all()), 10000)
    platform_course_count = max(Course.objects.count(), 25)
    seo = {
        "title": "EduPlanet | Python course Uzbekistan, Django course online va Backend course Tashkent",
        "description": "EduPlanet - Asilbek Mirolimovning Python, Django, REST API, PostgreSQL va DevOps bo'yicha content-rich LMS platformasi.",
        "keywords": global_keywords(["online lms", "uzbekistan coding academy", "personal brand educator"]),
        "og_title": "EduPlanet by Asilbek Mirolimov",
        "og_description": "Start your programming journey today with real-world backend and web development courses.",
        "og_image": courses[0].image if courses else UNSPLASH["backend"],
        "structured_data": build_structured_data({
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Organization",
                    "name": "EduPlanet",
                    "url": request.build_absolute_uri(reverse("dashboard")),
                    "logo": request.build_absolute_uri("/static/assets/images/logo_eduplanet_with_text.svg"),
                    "description": "EduPlanet is a production-ready LMS and personal brand platform by Asilbek Mirolimov.",
                },
                {
                    "@type": "Person",
                    "name": "Asilbek Mirolimov",
                    "jobTitle": "Senior Software Engineer & Educator",
                    "url": request.build_absolute_uri(reverse("dashboard")),
                    "knowsAbout": ["Python", "Django", "REST API", "PostgreSQL", "DevOps basics"],
                },
                {
                    "@type": "ItemList",
                    "name": "Featured Courses",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": index + 1,
                            "url": request.build_absolute_uri(reverse("course_detail", args=[course.slug])),
                            "name": course.name,
                        }
                        for index, course in enumerate(Course.objects.filter(featured=True)[:6])
                    ],
                },
            ]
        }),
    }
    context = {
        **build_common_context(request, seo),
        "featured_courses": courses,
        "centers": centers,
        "categories": categories,
        "latest_blogs": blogs,
        "testimonials": testimonials,
        "instructor": instructor,
        "stats": {
            "students": f"{total_students}+",
            "courses": f"{platform_course_count}+",
            "rating": "4.9",
            "hours": f"{total_hours}+",
        },
        "contact_email": INSTRUCTOR_DATA["email"],
        "contact_phone": "+998 90 979 34 50",
        "contact_location": "Tashkent, Uzbekistan",
        "og_image": courses[0].image if courses else UNSPLASH["backend"],
        **build_homepage_extras(lang, courses, all_courses, centers, blogs),
    }
    return context


def get_blog_list_context(request):
    ensure_platform_content()
    lang = get_language(request)
    blogs = [annotate_blog(blog, lang) for blog in BlogPost.objects.all()]
    seo = {
        "title": "EduPlanet Blog | Python, Django va Backend bo'yicha chuqur maqolalar",
        "description": "Asilbek Mirolimov tomonidan yozilgan SEO-optimized bloglar: Python roadmap, Django vs Flask, backend career va product engineering mavzulari.",
        "keywords": global_keywords(["backend blog", "python roadmap article", "django vs flask"]),
        "og_title": "EduPlanet Blog",
        "og_description": "In-depth articles on Python, Django, backend engineering, and developer growth.",
        "og_image": blogs[0].cover_image if blogs else UNSPLASH["workspace"],
        "structured_data": build_structured_data({
            "@context": "https://schema.org",
            "@type": "Blog",
            "name": "EduPlanet Blog",
            "url": request.build_absolute_uri(reverse("blog_list")),
            "blogPost": [
                {
                    "@type": "BlogPosting",
                    "headline": blog.title,
                    "datePublished": blog.published_at.isoformat(),
                    "author": {"@type": "Person", "name": blog.author_name},
                    "url": request.build_absolute_uri(reverse("blog_detail", args=[blog.slug])),
                }
                for blog in BlogPost.objects.all()[:10]
            ],
        }),
    }
    return {**build_common_context(request, seo), "blogs": blogs}


def get_blog_detail_context(request, blog):
    ensure_platform_content()
    lang = get_language(request)
    blog = annotate_blog(blog, lang)
    related_posts = [annotate_blog(item, lang) for item in BlogPost.objects.exclude(pk=blog.pk)[:3]]
    seo = {
        "title": blog.seo_title or blog.title,
        "description": blog.seo_description or blog.excerpt,
        "keywords": blog.meta_keywords or global_keywords([blog.topic]),
        "og_title": blog.seo_title or blog.title,
        "og_description": blog.seo_description or blog.excerpt,
        "og_image": blog.cover_image,
        "structured_data": build_structured_data({
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": blog.title,
            "description": blog.seo_description or blog.excerpt,
            "image": blog.cover_image,
            "datePublished": blog.published_at.isoformat(),
            "author": {"@type": "Person", "name": blog.author_name},
            "mainEntityOfPage": request.build_absolute_uri(),
        }),
    }
    return {**build_common_context(request, seo), "blog": blog, "related_posts": related_posts}


def get_centers_by_category_context(request, category):
    ensure_platform_content()
    lang = get_language(request)
    category = annotate_category(category, lang)
    centers = [annotate_center(center, lang) for center in LearningCenter.objects.filter(categories=category.id).prefetch_related("categories")]
    seo = {
        "title": f"{category.display_name} kurslari va yo'nalishlari | EduPlanet",
        "description": category.display_description,
        "keywords": global_keywords([category.display_name, "learning center", "online courses"]),
        "og_title": f"{category.display_name} | EduPlanet",
        "og_description": category.display_description,
        "og_image": centers[0].image if centers else UNSPLASH["learning"],
        "structured_data": build_structured_data({
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": category.display_name,
            "description": category.display_description,
        }),
    }
    return {**build_common_context(request, seo), "category": category, "learning_centers": centers}


def get_center_detail_context(request, center):
    ensure_platform_content()
    lang = get_language(request)
    center = annotate_center(center, lang)
    courses = [annotate_course(course, lang) for course in center.courses.all()]
    seo = {
        "title": center.seo_title or f"{center.name} | EduPlanet",
        "description": center.seo_description or center.description[:160],
        "keywords": center.meta_keywords or global_keywords([center.name]),
        "og_title": center.name,
        "og_description": center.description[:160],
        "og_image": center.image,
        "structured_data": build_structured_data({
            "@context": "https://schema.org",
            "@type": "EducationalOrganization",
            "name": center.name,
            "description": center.description,
            "url": request.build_absolute_uri(),
            "hasCourse": [
                {"@type": "Course", "name": course.name}
                for course in center.courses.all()
            ],
        }),
    }
    return {**build_common_context(request, seo), "learning_center": center, "courses": courses}


def get_course_detail_context(request, course, is_user_enrolled):
    ensure_platform_content()
    lang = get_language(request)
    course = annotate_course(course, lang)
    center = annotate_center(course.learning_center, lang)
    videos = list(course.video_contents.all())
    first_video = videos[0] if videos else None
    seo = {
        "title": course.seo_title or course.name,
        "description": course.seo_description or course.description[:160],
        "keywords": course.meta_keywords or global_keywords([course.name]),
        "og_title": course.name,
        "og_description": course.description[:160],
        "og_image": course.image,
        "structured_data": build_structured_data({
            "@context": "https://schema.org",
            "@type": "Course",
            "name": course.name,
            "description": course.description,
            "provider": {"@type": "Organization", "name": "EduPlanet"},
            "educationalLevel": course.level,
            "timeRequired": course.duration,
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": str(course.rating),
                "reviewCount": max(course.students_count // 8, 25),
            },
        }),
    }
    return {
        **build_common_context(request, seo),
        "course": course,
        "learning_center": center,
        "video_contents": videos,
        "first_video": first_video,
        "is_user_enrolled": is_user_enrolled,
        "preview_videos": [video for video in videos if video.is_preview],
    }


def get_contact_success_context(request):
    ensure_platform_content()
    lang = get_language(request)
    ui = UI_COPY[lang]
    seo = {
        "title": ui["contact_success_title"],
        "description": ui["contact_success_description"],
        "keywords": global_keywords(["contact", "mentorship", "course consultation"]),
        "og_title": ui["contact_success_title"],
        "og_description": ui["contact_success_description"],
        "og_image": UNSPLASH["mentor"],
        "structured_data": build_structured_data({
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "name": ui["contact_success_title"],
        }),
    }
    return {**build_common_context(request, seo)}
