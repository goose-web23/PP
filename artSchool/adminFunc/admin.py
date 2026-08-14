from django.contrib import admin
from .models import News, NewsPhoto, Notes
# Register your models here.
admin.site.register(News)
admin.site.register(NewsPhoto)
admin.site.register(Notes)