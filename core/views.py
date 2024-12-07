from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .models import Team, Employee, Aircraft, Part
from .serializers import TeamSerializer, EmployeeSerializer, AircraftSerializer, PartSerializer
from .permissions import IsTeamMember, IsMontajTeam

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view


from .models import Part, AIRCRAFT_TYPE_CHOICES


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
        responses={201: 'Uçak üretildi',
                   400: 'Eksik parça veya geçersiz uçak tipi'},
        description="Belirtilen uçak tipinin parçalarını monte eder."
    )
    @action(methods=['post'], detail=False, url_path='montaj', permission_classes=[IsMontajTeam])
    def montaj(self, request):
        aircraft_type = request.data.get('aircraft_type')
        if aircraft_type not in ['TB2', 'TB3', 'AKINCI', 'KIZILELMA']:
            return Response({"error": "Geçersiz uçak tipi"}, status=status.HTTP_400_BAD_REQUEST)

        required_parts = ['KANAT', 'GOVDE', 'KUYRUK', 'AVIYONIK']
        for p_type in required_parts:
            if not Part.objects.filter(part_type=p_type, used=False, aircraft__isnull=True).exists():
                return Response({"error": f"{p_type} tipi parça eksik."}, status=status.HTTP_400_BAD_REQUEST)

        new_aircraft = Aircraft.objects.create(aircraft_type=aircraft_type)

        for p_type in required_parts:
            part = Part.objects.filter(
                part_type=p_type, used=False, aircraft__isnull=True).first()
            part.aircraft = new_aircraft
            part.used = True
            part.save()

        return Response({"success": f"{new_aircraft.get_aircraft_type_display()} uçağı başarıyla üretildi!"}, status=status.HTTP_201_CREATED)


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.select_related('team').all()
    serializer_class = PartSerializer
    permission_classes = [IsTeamMember]

    # Geri dönüşüm için özel bir action
    @action(detail=True, methods=['delete'])
    def recycle(self, request, pk=None):
        try:
            part = self.get_object()
            part.delete()
            return Response({"success": f"{part.part_type} başarıyla geri dönüştürüldü."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Bir hata oluştu."}, status=status.HTTP_400_BAD_REQUEST)


def login_page(request):
    return render(request, 'login.html')


@login_required
def dashboard(request):
    user = request.user
    employee = getattr(user, 'employee', None)
    can_produce = False
    team_info = None

    if employee:
        team = employee.team
        if team:
            team_info = team.name  # Kullanıcının takım adı
            if team.team_type == 'MONTAJ_TAKIMI':
                # Montajcı tüm parçaları ve uçakları görebilmeli
                parts = Part.objects.select_related('team').all()
                aircrafts = Aircraft.objects.all()
            else:
                # Diğer personel sadece kendi türüne ait parçaları görmeli
                parts = Part.objects.select_related('team').filter(
                    part_type=team.team_type.replace('_TAKIMI', '')
                )
                aircrafts = None

                # Eğer takım parça üretimi yapabilen bir takım ise can_produce True olmalı
                if team.team_type in ['KANAT_TAKIMI', 'GOVDE_TAKIMI', 'KUYRUK_TAKIMI', 'AVIYONIK_TAKIMI']:
                    can_produce = True
        else:
            parts = None
            aircrafts = None
    else:
        parts = None
        aircrafts = None

    context = {
        'parts': parts,
        'aircrafts': aircrafts,
        'employee': employee,
        'can_produce': can_produce,
        'aircraft_type_choices': AIRCRAFT_TYPE_CHOICES,
        'team_info': team_info if team_info else "Takımsız",  # Takım adı context'e eklendi
    }

    return render(request, 'dashboard.html', context)



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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def produce_part(request):
    employee = getattr(request.user, 'employee', None)
    if not employee or not employee.team:
        return Response({'error': 'Yetkisiz kullanıcı.'}, status=status.HTTP_403_FORBIDDEN)

    part_type = employee.team.team_type.replace('_TAKIMI', '')
    target_aircraft_type = request.data.get('target_aircraft_type')

    if not target_aircraft_type or target_aircraft_type not in [choice[0] for choice in AIRCRAFT_TYPE_CHOICES]:
        return Response({'error': 'Geçersiz uçak tipi.'}, status=status.HTTP_400_BAD_REQUEST)

    # Parça üretimi
    part = Part.objects.create(
        part_type=part_type,
        team=employee.team,
        target_aircraft_type=target_aircraft_type,
        used=False
    )

    # JSON formatında üretim zamanını döndürdüğünüzden emin olun
    return Response({
        'success': f'{part_type} parçası başarıyla üretildi.',
        'part_type_display': part.get_part_type_display(),
        'target_aircraft_type_display': part.get_target_aircraft_type_display(),
        'team_name': part.team.name,
        'production_time': part.production_time.strftime('%Y-%m-%d %H:%M:%S'),  # Tarih formatı
        'id': part.id
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recycle_part(request):
    employee = getattr(request.user, 'employee', None)
    if not employee or not employee.team:
        return Response({'error': 'Yetkisiz kullanıcı.'}, status=status.HTTP_403_FORBIDDEN)

    part_id = request.data.get('part_id')

    if not part_id:
        return Response({'error': 'Parça ID belirtilmedi.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Belirtilen ID ile parçayı bul
        part = Part.objects.get(id=part_id)
        
        # Kullanıcının takımı ile parçanın takımı uyumsuzsa
        if part.team != employee.team:
            return Response({'error': 'Sadece kendi takımınızın ürettiği parçayı geri dönüşüme yollayabilirsiniz.'}, status=status.HTTP_403_FORBIDDEN)

        part.delete()  # Parçayı geri dönüştür (sil)
        return Response({'success': 'Parça başarıyla geri dönüştürüldü.'}, status=status.HTTP_200_OK)
    except Part.DoesNotExist:
        return Response({'error': 'Belirtilen parça bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Bir hata oluştu: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)