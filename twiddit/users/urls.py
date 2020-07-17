from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('user/<str:username>/follow/', views.follow_info, name='follow-info'),
    path('user/<str:username>/follow-toggle/', views.follow_toggle, name='follow-toggle'),
]