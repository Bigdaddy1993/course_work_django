from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='users/', verbose_name='изображение', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон')
    country = models.CharField(max_length=30, verbose_name='страна')
    token = models.CharField(max_length=10, verbose_name='верификация', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активно')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ('set_is_active',
             'can change is_active')
        ]
