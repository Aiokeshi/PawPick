from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .models import Review
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from main import views
from .forms import ReviewForm


# Create your views here.
def index(request):
    context= {
        'title': 'Home',
        'content': 'Главная страница'
    }
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Отзыв отправлен!")
            return redirect('main:index')
    else:
        review_form = ReviewForm()

    return render(request, 'main/index.html', {
        'review_form': review_form
    })