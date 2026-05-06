from django.urls import path

from catalog import views


app_name = 'catalog'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorite/<slug:card_slug>/', views.toggle_favorite, name='toggle_favorite'),
    path('card/<slug:card_slug>/', views.card, name='card'),
]
