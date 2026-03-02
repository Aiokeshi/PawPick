from django.contrib import admin
from django.urls import path,include
from catalog import views
app_name = 'catalog'
urlpatterns = [
    path('', views.catalog,name='catalog'),
    path('card/<slug:card_slug>/', views.card,name='card'),
]