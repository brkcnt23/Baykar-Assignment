
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    PartViewSet as CorePartViewSet,
    TeamViewSet as CoreTeamViewSet,
    EmployeeViewSet as CoreEmployeeViewSet,
    AircraftViewSet as CoreAircraftViewSet
)
from core.views import (
    PartViewSet,
    TeamViewSet,
    EmployeeViewSet,
    AircraftViewSet,
    login_user,
    login_page,
    dashboard,
)



router = DefaultRouter()
router.register(r'parts', PartViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'employee', EmployeeViewSet)
router.register(r'aircraft', AircraftViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin paneline erişmek için bu satırı ekleyin
    path('', include(router.urls)),
    path('login/', login_page, name='login'),  # Login sayfası için
    path('api/login', login_user, name='api_login'),  # Login işlemi için
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard için
]