from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_cover_image(self):
        cover_image = BlogImage.objects.filter(blog_post=self).first()
        return cover_image


class BlogImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return self.image_url
