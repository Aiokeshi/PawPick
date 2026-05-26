from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 20


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('main:index')

        messages.error(request, 'Неверный логин или пароль!')

    return render(request, 'register/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not email or not password or not confirm_password:
            messages.error(request, 'Все поля обязательны для заполнения!')
            return render(request, 'register/register.html')

        if len(username) < USERNAME_MIN_LENGTH:
            messages.error(request,f'Логин должен быть не короче {USERNAME_MIN_LENGTH} символов.')
            return render(request, 'register/register.html')

        if len(username) > USERNAME_MAX_LENGTH:
            messages.error(request,f'Логин должен быть не длиннее {USERNAME_MAX_LENGTH} символов.')
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
            email=email,
            password=password_hash
        )

        login(request, user)

        return redirect('main:index')

    return render(request, 'register/register.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('register:login')
