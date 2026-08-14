from django.shortcuts import render, get_object_or_404, redirect
import re
from django.contrib.auth.hashers import make_password
from users.models import User, Teacher, Student
from .models import News, NewsPhoto, Notes
from django.contrib import messages
from django.core.paginator import Paginator

def news_list_page(request):
    ordering = request.GET.get('ordering', '-date')
    news_list = News.objects.all().order_by(ordering)
    
    paginator = Paginator(news_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news_list.html', {
        'news_list': page_obj,
        'ordering': ordering,
    })

def news_detail_page(request, news_id):
    news = get_object_or_404(News, id=news_id)
    photos = news.photos.all()
    is_admin = request.user.is_authenticated and request.user.role == 'admin'
    
    if request.method == 'POST' and is_admin:
        action = request.POST.get('action')
        if action == 'update':
            news.heading = request.POST.get('heading', news.heading)
            news.full_text = request.POST.get('full_text', news.full_text)
            news.save()
            new_photos = request.FILES.getlist('photos')
            for photo in new_photos:
                NewsPhoto.objects.create(new=news, photo=photo)
            messages.success(request, 'Новость обновлена')
            return redirect('news-list-page')
        elif action == 'delete':
            news.delete()
            messages.success(request, 'Новость удалена')
            return redirect('news-list-page')
    
    return render(request, 'news_detail.html', {
        'news': news,
        'photos': photos,
        'is_admin': is_admin,
    })

def notes_list_page(request):
    notes = Notes.objects.all()

    is_admin = request.user.is_authenticated and request.user.role == 'admin'
    
    if request.method == 'POST' and is_admin:
        note_id = request.POST.get('note_id')
        action = request.POST.get('action')
        if action == 'delete' and note_id:
            note = get_object_or_404(Notes, id=note_id)
            note.delete()
            messages.success(request, 'Ноты удалены')
            return redirect('notes-list-page')
        elif action == 'update' and note_id:
            note = get_object_or_404(Notes, id=note_id)
            note.heading = request.POST.get('heading', note.heading)
            note.class_number = request.POST.get('class_number', note.class_number)
            note.department = request.POST.get('department', note.department)
            new_file = request.FILES.get('file')
            if new_file:
                note.file = new_file
            note.save()
            messages.success(request, 'Ноты обновлены')
            return redirect('notes-list-page')
    
    department = request.GET.get('department')
    class_number = request.GET.get('class_number')
    
    if department:
        notes = notes.filter(department=department)
    if class_number:
        notes = notes.filter(class_number=class_number)
    
    paginator = Paginator(notes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'notes_list.html', {
        'notes': page_obj,
        'selected_department': department or '',
        'selected_class': class_number or '',
        'classes': range(1, 10),
    })
def notes_detail_page(request, note_id):
    note = get_object_or_404(Notes, id=note_id)
    is_admin = request.user.is_authenticated and request.user.role == 'admin'

    if request.method == 'POST' and is_admin:
        action = request.POST.get('action')
        if action == 'update':
            note.heading = request.POST.get('heading', note.heading)
            note.class_number = request.POST.get('class_number', note.class_number)
            note.department = request.POST.get('department', note.department)
            new_file = request.FILES.get('file')
            if new_file:
                note.file = new_file
            note.save()
            messages.success(request, 'Ноты обновлены')
            return redirect('notes-list-page')
        elif action == 'delete':
            note.delete()
            messages.success(request, 'Ноты удалены')
            return redirect('notes-list-page')

    return render(request, 'notes_detail.html', {
        'note': note,
        'classes': range(1, 10),
        'is_admin': is_admin,
    })

def handle_create_user(request):
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    role = request.POST.get('role', '')

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Логин уже существует')
        return redirect('profile-page')

    user = User.objects.create(username=username, password=make_password(password), role=role)

    if role == 'teacher':
        Teacher.objects.create(
            user=user,
            full_name=request.POST.get('full_name', ''),
            age=int(request.POST.get('age', 0) or 0),
            department=request.POST.get('department', 'music'),
            experience=float(request.POST.get('experience', 0) or 0),
        )
    elif role == 'student':
        student = Student.objects.create(
            user=user,
            full_name=request.POST.get('full_name', ''),
            department=request.POST.get('department', 'music'),
            class_number=int(request.POST.get('class_number', 0) or 0),
        )
        teacher_id = request.POST.get('teacher_id', '')
        if teacher_id:
            student.teacher = Teacher.objects.get(id=teacher_id)
            student.save()

    messages.success(request, f'Пользователь {username} создан')
    return redirect('profile-page')


def handle_update_user(request):
    user_id = request.POST.get('user_id')
    user = User.objects.get(id=user_id)

    new_password = request.POST.get('password', '')
    if new_password:
        user.password = make_password(new_password)
    user.save()

    if user.role == 'teacher':
        teacher = user.teacher_profile
        teacher.full_name = request.POST.get('full_name', teacher.full_name)
        teacher.department = request.POST.get('department', teacher.department)
        teacher.save()
    elif user.role == 'student':
        student = user.student_profile
        student.full_name = request.POST.get('full_name', student.full_name)
        student.department = request.POST.get('department', student.department)
        student.class_number = int(request.POST.get('class_number', student.class_number))
        teacher_id = request.POST.get('teacher_id', '')
        if teacher_id:
            student.teacher = Teacher.objects.get(id=teacher_id)
        student.save()

    messages.success(request, 'Пользователь обновлён')
    return redirect('profile-page')


def handle_delete_user(request):
    user_id = request.POST.get('user_id')
    user = User.objects.get(id=user_id)
    if user == request.user:
        messages.error(request, 'Нельзя удалить самого себя')
    else:
        user.delete()
        messages.success(request, 'Пользователь удалён')
    return redirect('profile-page')


def handle_create_news(request):
    heading = request.POST.get('heading', '').strip()
    full_text = request.POST.get('full_text', '').strip()

    news = News.objects.create(heading=heading, full_text=full_text)
    photos = request.FILES.getlist('photos')
    for photo in photos:
        NewsPhoto.objects.create(new=news, photo=photo)

    messages.success(request, 'Новость создана')
    return redirect('profile-page')


def handle_create_notes(request):
    heading = request.POST.get('heading', '').strip()
    class_number = request.POST.get('class_number')
    department = request.POST.get('department')
    file = request.FILES.get('file')

    Notes.objects.create(heading=heading, class_number=int(class_number), department=department, file=file)
    messages.success(request, 'Ноты добавлены')
    return redirect('profile-page')


def handle_admin_post(request):
    form_type = request.POST.get('form_type')
    if form_type == 'create_user':
        return handle_create_user(request)
    elif form_type == 'update_user':
        return handle_update_user(request)
    elif form_type == 'delete_user':
        return handle_delete_user(request)
    elif form_type == 'create_news':
        return handle_create_news(request)
    elif form_type == 'create_notes':
        return handle_create_notes(request)
    return redirect('profile-page')