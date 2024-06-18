from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    """Менеджер пользователя реализующий создание пользователя по email"""

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Модель пользователя"""
    username = models.CharField(max_length=100, unique=True, verbose_name='username')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='email')
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='имя')
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='фамилия')

    account_status = models.CharField(max_length=100, null=True, blank=True, verbose_name='статус')
    image = models.ImageField(upload_to='profile_image/%Y/%m/%d/', null=True, blank=True, verbose_name='аватарка')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    def __str__(self):
        return self.username
