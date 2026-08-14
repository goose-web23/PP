from django.db import models

# Create your models here.
class Notes(models.Model):
    CLASS_CHOICES = [(i, str(i)) for i in range(10)]
    DEPARTMENT_CHOICES = [
        ('piano', 'Фортепиано'),
        ('guitar', 'Гитара'),
        ('vocal', 'Вокальное'),
        ('accordion', 'Баян'),
        ('balalaika', 'Домра'),
    ]

    heading = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    class_number = models.IntegerField(
        choices=CLASS_CHOICES,
        verbose_name='Класс'
    )
    department = models.CharField(
        choices=DEPARTMENT_CHOICES,
        max_length=40,
        verbose_name='Отделение'
    )
    file = models.FileField(
        upload_to='notes/',
        verbose_name='Файл нот'
    )
    def __str__(self):
        return super().__str__()

class News(models.Model):
    heading = models.CharField(
        max_length=255,
        verbose_name='Заголовок'
    )
    full_text = models.TextField(
        verbose_name='Полный текст'
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    def __str__(self):
        return super().__str__()
    
class NewsPhoto(models.Model):
    new = models.ForeignKey(
        News, 
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Новость'
    )
    photo = models.ImageField(
        upload_to='news_photos/',
        verbose_name='Фото'
    )
    def __str__(self):
        return super().__str__()