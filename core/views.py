from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from .models import Team, Employee, Aircraft, Part
from .serializers import TeamSerializer, EmployeeSerializer, AircraftSerializer,PartSerializer
from .permissions import IsTeamMember, IsMontajTeam
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

@extend_schema(description="Uçak üretimi için Montaj takımı gerekli.")
class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

    @extend_schema(
        request={
            'application/json': {
                'aircraft_type': 'str'
            }
        },
        responses={201: 'Uçak üretildi', 400: 'Eksik parça veya geçersiz uçak tipi'},
        description="Belirtilen uçak tipinin parçalarını monte eder."
    )
    @action(methods=['post'], detail=False, url_path='montaj', permission_classes=[IsMontajTeam])
    def montaj(self, request):
        aircraft_type = request.data.get('aircraft_type')
        if aircraft_type not in ['TB2', 'TB3', 'AKINCI', 'KIZILELMA']:
            return Response({"error": "Geçersiz uçak tipi"}, status=status.HTTP_400_BAD_REQUEST)

        required_parts = ['KANAT', 'GOVDE', 'KUYRUK', 'AVIYONIK']
        for p_tipi in required_parts:
            if not Part.objects.filter(part_type=p_tipi, used=False, aircraft__isnull=True).exists():
                return Response({"error": f"{p_tipi} tipi parça eksik."}, status=status.HTTP_400_BAD_REQUEST)

        new_aircraft = Aircraft.objects.create(aircraft_type=aircraft_type)

        for p_tipi in required_parts:
            part = Part.objects.filter(part_type=p_tipi, used=False, aircraft__isnull=True).first()
            part.aircraft = new_aircraft
            part.used = True
            part.save()

        return Response({"success": f"{new_aircraft.get_aircraft_type_display()} uçağı başarıyla üretildi!"}, status=status.HTTP_201_CREATED)

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsTeamMember]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['part_type', 'team', 'aircraft', 'used']

    def get_queryset(self):
        employee = getattr(self.request.user, 'employee', None)
        qs = Part.objects.all()
        if employee and employee.team:
            qs = qs.filter(team=employee.team)
        return qs
    
def login_page(request):
    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid credentials'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})