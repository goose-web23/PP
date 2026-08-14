from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout

def home_page(request):
    return render(request, 'home.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('profile-page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Вы вошли!')
            return redirect('profile-page')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'login.html')

def school_info_page(request):
    return render(request, 'school_info.html')

def departments_page(request):
    return render(request, 'departments.html')

def for_parents_page(request):
    return render(request, 'for_parents.html')

from django.contrib.auth import logout as auth_logout

def logout_view(request):
    auth_logout(request)
    return redirect('home')