from django.db import models
from users.models import Student, Teacher
# Create your models here.

class ExamResults(models.Model):
    MARK_CHOICES = [
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    heading = models.CharField(
        max_length=255,
        verbose_name='Название экамена'
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='exam_results',
        verbose_name='Ученик'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='given_marks',
        verbose_name='Учитель'
    )
    date = models.DateField(
        verbose_name='Дата экзамена'
    )
    mark = models.IntegerField(
        choices=MARK_CHOICES,
        verbose_name='Оценка'
    )

    def __str__(self):
        return super().__str__()

class Diploma(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='diplomas',
        verbose_name='Ученик'
    )
    file = models.FileField(
        upload_to='diplomas/',
        verbose_name='Файл грамоты'
    )
    def __str__(self):
        return super().__str__()