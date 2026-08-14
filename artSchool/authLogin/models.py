from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Ученик'),
        ('teacher', 'Учитель'),
        ('admin', 'Админ')
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name='Роль'
    )
    def __str__(self):
        return super().__str__()
