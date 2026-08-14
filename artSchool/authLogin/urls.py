from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('login/', views.login_page, name='login-page'),
    path('school-info/', views.school_info_page, name='school-info'),
    path('departments/', views.departments_page, name='departments'),
    path('for-parents/', views.for_parents_page, name='for-parents'),
    path('logout/', views.logout_view, name='logout-page'),
]