from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('api/login', views.login_user, name='api_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
]
