from django import forms

from blogs.models import BlogImage, BlogPost
from centers.models import Category, LearningCenter
from connections.models import Testimonial
from courses.models import Course, VideoContent
from users.models import ContactUs, InstructorProfile, User


INPUT = 'form-control'
TEXTAREA = 'form-control'
SELECT = 'form-control'
CHECK = 'form-check-input'


def _attrs(extra=None, css=INPUT):
    base = {'class': css}
    if extra:
        base.update(extra)
    return base


class AdminLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs=_attrs({'placeholder': 'Username', 'autofocus': 'autofocus'})),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=_attrs({'placeholder': 'Parol'})),
    )


class UserAdminForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs=_attrs({'placeholder': "Yangi parol (bo'sh qoldirsangiz o'zgarmaydi)"})),
        label='Parol',
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'phone_number',
            'image', 'is_active', 'is_staff', 'is_superuser',
        )
        widgets = {
            'username': forms.TextInput(attrs=_attrs()),
            'first_name': forms.TextInput(attrs=_attrs()),
            'last_name': forms.TextInput(attrs=_attrs()),
            'email': forms.EmailInput(attrs=_attrs()),
            'phone_number': forms.TextInput(attrs=_attrs({'placeholder': '+998901234567'})),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'is_active': forms.CheckboxInput(attrs={'class': CHECK}),
            'is_staff': forms.CheckboxInput(attrs={'class': CHECK}),
            'is_superuser': forms.CheckboxInput(attrs={'class': CHECK}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = InstructorProfile
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs=_attrs(css=SELECT)),
            'title': forms.TextInput(attrs=_attrs()),
            'bio': forms.Textarea(attrs=_attrs({'rows': 3}, css=TEXTAREA)),
            'mission': forms.Textarea(attrs=_attrs({'rows': 3}, css=TEXTAREA)),
            'profile_description': forms.Textarea(attrs=_attrs({'rows': 3}, css=TEXTAREA)),
            'experience_years': forms.NumberInput(attrs=_attrs()),
            'skills': forms.Textarea(attrs=_attrs({'rows': 2, 'placeholder': '["Python","Django"]'}, css=TEXTAREA)),
            'location': forms.TextInput(attrs=_attrs()),
            'website': forms.URLInput(attrs=_attrs()),
            'linkedin': forms.URLInput(attrs=_attrs()),
            'github': forms.URLInput(attrs=_attrs()),
            'telegram': forms.URLInput(attrs=_attrs()),
            'avatar_url': forms.URLInput(attrs=_attrs()),
            'translations': forms.Textarea(attrs=_attrs({'rows': 2, 'placeholder': '{}'}, css=TEXTAREA)),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'icon', 'translations', 'slug')
        widgets = {
            'name': forms.TextInput(attrs=_attrs()),
            'description': forms.Textarea(attrs=_attrs({'rows': 3}, css=TEXTAREA)),
            'icon': forms.TextInput(attrs=_attrs({'placeholder': 'mdi-school'})),
            'translations': forms.Textarea(attrs=_attrs({'rows': 2, 'placeholder': '{}'}, css=TEXTAREA)),
            'slug': forms.TextInput(attrs=_attrs({'placeholder': "Bo'sh qoldirilsa avtomatik yaratiladi"})),
        }


class LearningCenterForm(forms.ModelForm):
    class Meta:
        model = LearningCenter
        fields = (
            'name', 'headline', 'description', 'categories', 'location', 'email',
            'phone_number', 'image', 'website', 'students_count', 'mentors_count',
            'courses_count', 'features', 'translations', 'seo_title',
            'seo_description', 'meta_keywords', 'slug',
        )
        widgets = {
            'name': forms.TextInput(attrs=_attrs()),
            'headline': forms.TextInput(attrs=_attrs()),
            'description': forms.Textarea(attrs=_attrs({'rows': 4}, css=TEXTAREA)),
            'categories': forms.SelectMultiple(attrs=_attrs(css=SELECT)),
            'location': forms.TextInput(attrs=_attrs()),
            'email': forms.EmailInput(attrs=_attrs()),
            'phone_number': forms.TextInput(attrs=_attrs({'placeholder': '+998901234567'})),
            'image': forms.URLInput(attrs=_attrs()),
            'website': forms.URLInput(attrs=_attrs()),
            'students_count': forms.NumberInput(attrs=_attrs()),
            'mentors_count': forms.NumberInput(attrs=_attrs()),
            'courses_count': forms.NumberInput(attrs=_attrs()),
            'features': forms.Textarea(attrs=_attrs({'rows': 2, 'placeholder': '[]'}, css=TEXTAREA)),
            'translations': forms.Textarea(attrs=_attrs({'rows': 2, 'placeholder': '{}'}, css=TEXTAREA)),
            'seo_title': forms.TextInput(attrs=_attrs()),
            'seo_description': forms.Textarea(attrs=_attrs({'rows': 2}, css=TEXTAREA)),
            'meta_keywords': forms.TextInput(attrs=_attrs()),
            'slug': forms.TextInput(attrs=_attrs()),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = (
            'name', 'subtitle', 'description', 'learning_center', 'image', 'level',
            'duration', 'lessons_count', 'students_count', 'hours_watched', 'price',
            'highlights', 'outcomes', 'curriculum', 'translations', 'seo_title',
            'seo_description', 'meta_keywords', 'featured', 'slug',
        )
        widgets = {
            'name': forms.TextInput(attrs=_attrs()),
            'subtitle': forms.TextInput(attrs=_attrs()),
            'description': forms.Textarea(attrs=_attrs({'rows': 4}, css=TEXTAREA)),
            'learning_center': forms.Select(attrs=_attrs(css=SELECT)),
            'image': forms.URLInput(attrs=_attrs()),
            'level': forms.TextInput(attrs=_attrs({'placeholder': 'Boshlang\'ich / O\'rta / Yuqori'})),
            'duration': forms.TextInput(attrs=_attrs({'placeholder': '8 hafta'})),
            'lessons_count': forms.NumberInput(attrs=_attrs()),
            'students_count': forms.NumberInput(attrs=_attrs()),
            'hours_watched': forms.NumberInput(attrs=_attrs()),
            'price': forms.NumberInput(attrs=_attrs()),
            'highlights': forms.Textarea(attrs=_attrs({'rows': 2, 'placeholder': '[]'}, css=TEXTAREA)),
            'outcomes': forms.Textarea(attrs=_attrs({'rows': 2, 'placeholder': '[]'}, css=TEXTAREA)),
            'curriculum': forms.Textarea(attrs=_attrs({'rows': 2, 'placeholder': '[]'}, css=TEXTAREA)),
            'translations': forms.Textarea(attrs=_attrs({'rows': 2, 'placeholder': '{}'}, css=TEXTAREA)),
            'seo_title': forms.TextInput(attrs=_attrs()),
            'seo_description': forms.Textarea(attrs=_attrs({'rows': 2}, css=TEXTAREA)),
            'meta_keywords': forms.TextInput(attrs=_attrs()),
            'featured': forms.CheckboxInput(attrs={'class': CHECK}),
            'slug': forms.TextInput(attrs=_attrs()),
        }


class VideoContentForm(forms.ModelForm):
    class Meta:
        model = VideoContent
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs=_attrs()),
            'description': forms.Textarea(attrs=_attrs({'rows': 3}, css=TEXTAREA)),
            'course': forms.Select(attrs=_attrs(css=SELECT)),
            'cover_image': forms.URLInput(attrs=_attrs()),
            'video_url': forms.URLInput(attrs=_attrs()),
            'duration': forms.TextInput(attrs=_attrs()),
            'sort_order': forms.NumberInput(attrs=_attrs()),
            'is_preview': forms.CheckboxInput(attrs={'class': CHECK}),
        }


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = (
            'title', 'slug', 'excerpt', 'content', 'author_name', 'cover_image',
            'reading_time', 'topic', 'seo_title', 'seo_description', 'meta_keywords',
            'translations', 'published_at', 'featured',
        )
        widgets = {
            'title': forms.TextInput(attrs=_attrs()),
            'slug': forms.TextInput(attrs=_attrs()),
            'excerpt': forms.Textarea(attrs=_attrs({'rows': 3}, css=TEXTAREA)),
            'content': forms.Textarea(attrs=_attrs({'rows': 10}, css=TEXTAREA)),
            'author_name': forms.TextInput(attrs=_attrs()),
            'cover_image': forms.URLInput(attrs=_attrs()),
            'reading_time': forms.NumberInput(attrs=_attrs()),
            'topic': forms.TextInput(attrs=_attrs()),
            'seo_title': forms.TextInput(attrs=_attrs()),
            'seo_description': forms.Textarea(attrs=_attrs({'rows': 2}, css=TEXTAREA)),
            'meta_keywords': forms.TextInput(attrs=_attrs()),
            'translations': forms.Textarea(attrs=_attrs({'rows': 2, 'placeholder': '{}'}, css=TEXTAREA)),
            'published_at': forms.DateInput(attrs=_attrs({'type': 'date'})),
            'featured': forms.CheckboxInput(attrs={'class': CHECK}),
        }


class BlogImageForm(forms.ModelForm):
    class Meta:
        model = BlogImage
        fields = '__all__'
        widgets = {
            'blog_post': forms.Select(attrs=_attrs(css=SELECT)),
            'image_url': forms.URLInput(attrs=_attrs()),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs=_attrs()),
            'role': forms.TextInput(attrs=_attrs()),
            'quote': forms.Textarea(attrs=_attrs({'rows': 3}, css=TEXTAREA)),
            'avatar_url': forms.URLInput(attrs=_attrs()),
            'rating': forms.NumberInput(attrs=_attrs({'step': '0.1'})),
            'sort_order': forms.NumberInput(attrs=_attrs()),
            'translations': forms.Textarea(attrs=_attrs({'rows': 2, 'placeholder': '{}'}, css=TEXTAREA)),
        }


class ContactUsResponseForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('full_name', 'email', 'phone_number', 'message')
        widgets = {
            'full_name': forms.TextInput(attrs=_attrs({'readonly': True})),
            'email': forms.EmailInput(attrs=_attrs({'readonly': True})),
            'phone_number': forms.TextInput(attrs=_attrs({'readonly': True})),
            'message': forms.Textarea(attrs=_attrs({'rows': 6, 'readonly': True}, css=TEXTAREA)),
        }
