
from django.contrib import admin
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
    produce_part,
    recycle_part,
    produce_aircraft,
)



router = DefaultRouter()
router.register(r'aircraft', AircraftViewSet, basename='aircraft')
router.register(r'parts', PartViewSet, basename='part')

router.register(r'teams', TeamViewSet)
router.register(r'employee', EmployeeViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),  # Admin paneline erişmek için gerekli url
    path('', include(router.urls)),
    path('login/', login_page, name='login'),  # Login sayfası için
    path('api/login', login_user, name='api_login'),  # Login işlemi için
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard için
    path('api/produce-part/', produce_part, name='produce_part'), # Parça üretimi için
    path('api/recycle-part/', recycle_part, name='recycle_part'), # Geri dönüşüm için
    path('api/produce-aircraft/', produce_aircraft, name='produce_aircraft'), # Hava aracı üretimi için
]