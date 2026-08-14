from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_list_page, name='news-list-page'),
    path('news/<int:news_id>/', views.news_detail_page, name='news-detail-page'),
    path('notes/', views.notes_list_page, name='notes-list-page'),
    path('notes/<int:note_id>/', views.notes_detail_page, name='notes-detail-page'),
]