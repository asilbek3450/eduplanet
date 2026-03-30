from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class BlogPost(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    author_name = models.CharField(max_length=128, default='Asilbek Mirolimov')
    cover_image = models.URLField(blank=True)
    reading_time = models.PositiveSmallIntegerField(default=6)
    topic = models.CharField(max_length=120, blank=True)
    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    translations = models.JSONField(default=dict, blank=True)
    published_at = models.DateField(default=timezone.now)
    featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.seo_title:
            self.seo_title = self.title
        if not self.seo_description and self.excerpt:
            self.seo_description = self.excerpt[:160]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_cover_image(self):
        if self.cover_image:
            return self.cover_image
        cover_image = BlogImage.objects.filter(blog_post=self).first()
        return cover_image.image_url if cover_image else ''


class BlogImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()

    def __str__(self):
        return self.image_url
