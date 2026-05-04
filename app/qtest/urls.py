from django.urls import path

from . import views


app_name = 'qtest'

urlpatterns = [
    path('test/', views.test_start, name='test_start'),
    path('test/<int:step>/', views.test_step, name='test_step'),
    path('test/result/', views.test_result, name='test_result'),
    path('profile/', views.profile, name='profile'),
]
