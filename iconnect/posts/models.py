from django.contrib.auth import get_user_model
from django.db import models
from django.utils.safestring import mark_safe

user = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(user, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/')
    description = models.TextField()
    is_archive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(user, blank=True, related_name='user_likes')
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-updated_at', '-created_at']
    
    def __str__(self):
        return self.description[:12]

    def thumbnail(self):
        return mark_safe(f'<img src="/media/{self.image}" width="150" />')
    
    
