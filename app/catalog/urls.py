from django.contrib import admin
from django.urls import path,include
from catalog import views
app_name = 'catalog'
urlpatterns = [
    path('catalog/', views.catalog,name='catalog'),
    path('product/', views.product,name='product'),
]