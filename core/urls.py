from django.urls import path
from . import views

#core içerisinde gerekli yönlendirmelerin yapıldığı sınıf
urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('api/login', views.login_user, name='api_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/produce-part/', views.produce_part, name='produce_part'),
    path('api/recycle-part/', views.recycle_part, name='recycle_part'),
    
]