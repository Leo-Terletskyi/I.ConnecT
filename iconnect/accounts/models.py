from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/avatars/', null=True)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField('phone number', max_length=14, null=True)
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    def __str__(self):
        return self.username
    
