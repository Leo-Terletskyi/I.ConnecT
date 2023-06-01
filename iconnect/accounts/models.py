from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/avatars/', null=True)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField('phone number', max_length=14, null=True)
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
        
    @property
    def followers_count(self):
        return self.followers.all().count()
    
    @property
    def following_count(self):
        return self.following.all().count()
