from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from main import views
from main import urls

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('main:index')
        else:
            messages.error(request, 'Неверный логин или пароль!')
    return render(request, 'register/login.html')

def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        last_name = request.POST.get('name')
        email = request.POST.get('email')
        id = request.POST.get('tel')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
  
        if not username or not last_name or not email or not password or not confirm_password:
            messages.error(request, 'Все поля обязательны для заполнения!')
            return render(request, 'register/register.html')
   
        if password != confirm_password:
            messages.error(request, 'Пароли не совпадают!')
            return render(request, 'register/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким логином уже существует.')
            return render(request, 'register/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return render(request, 'register/register.html')
      
        password_hash = make_password(password)
    
        user = User.objects.create(
            username=username,
            last_name=last_name,
            email=email,
            password=password_hash  
        )
        
        login(request, user)

        return redirect('main:index') 

    return render(request, 'register/register.html') 

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('main:index')
