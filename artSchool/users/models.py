from django.db import models
from authLogin.models import User

# Create your models here.
class Teacher(models.Model):
    DEPARTMENT_CHOICES = [
        ('music', 'Музыкальное'),
        ('art', 'Художественное')
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name='ФИО'
    )
    age = models.IntegerField(
        verbose_name='Возраст'
    )
    department = models.CharField(
        choices=DEPARTMENT_CHOICES,
        max_length=20,
        verbose_name='Отделение'
    )
    experience = models.FloatField(
        verbose_name='Стаж'
    )
    def __str__(self):
        return super().__str__()

class Student(models.Model):
    DEPARTMENT_CHOICES = [
        ('music', 'Музыкальное'),
        ('art', 'Художественное')
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name='ФИО'
    )
    department = models.CharField(
        choices=DEPARTMENT_CHOICES,
        max_length=20,
        verbose_name='Отделение'
    )
    class_number = models.IntegerField(
        verbose_name='Класс'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='students',
        verbose_name='Учитель'
    )
    def __str__(self):
        return super().__str__()