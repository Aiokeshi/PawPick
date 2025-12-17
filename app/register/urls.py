from django.contrib import admin
from django.urls import path,include
from register import views
app_name = 'register'
urlpatterns = [
    path('login/', views.login_view,name='login'),
    path('register/', views.register,name='register'),
]