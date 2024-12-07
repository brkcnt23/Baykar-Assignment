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
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view


from .models import Part, AIRCRAFT_TYPE_CHOICES

"""
gerekli importlar oluşturuldu:
rest framework'ten gelen viewsetleri, action, response, IsAuthenticated
model dosyamızdan gelen takım, personel, hava aracı, parça bilgileri
giriş işlemlerini kontrol etmesi için auth ve login
web loop içerisinde gerekli sayfaların açılmasını sağlayan render
jsonresponse döndürülebilmesini ve gerektiğinde django filters kullanılmasını sağlayan importlar...
"""

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    permission_classes = [IsMontajTeam]

    @extend_schema(description="Üretilen uçakların listesini getir.")
    @action(methods=['get'], detail=False, url_path='list', permission_classes=[IsMontajTeam])
    def list_aircrafts(self, request):
        aircrafts = Aircraft.objects.all()
        serializer = self.get_serializer(aircrafts, many=True)
        return Response(serializer.data)


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

#login ekranı
def login_page(request):
    return render(request, 'login.html')

#dashboard ekranı
@login_required
def dashboard(request):
    user = request.user
    employee = getattr(user, 'employee', None)
    can_produce = False
    team_info = None
    ready_aircrafts = {}

    if employee:
        team = employee.team
        if team:
            team_info = team.name
            if team.team_type == 'MONTAJ_TAKIMI':
                parts = Part.objects.select_related('team').all()
                aircrafts = Aircraft.objects.all()
                can_produce = True

                # Üretime hazır uçaklar verisini oluşturma
                required_parts = {
                    "KANAT": 2,
                    "GOVDE": 1,
                    "KUYRUK": 1,
                    "AVIYONIK": 1,
                }
                for aircraft_type, _ in AIRCRAFT_TYPE_CHOICES:
                    available_parts = {part_type: 0 for part_type in required_parts}
                    for part_type in required_parts:
                        count = parts.filter(
                            part_type=part_type,
                            target_aircraft_type=aircraft_type,
                            used=False,
                            aircraft__isnull=True,
                        ).count()
                        available_parts[part_type] = count

                    # Eğer tüm parçalar yeterliyse listeye ekle
                    if all(
                        available_parts[part_type] >= count_needed
                        for part_type, count_needed in required_parts.items()
                    ):
                        ready_aircrafts[aircraft_type] = {
                            "required_parts": required_parts,
                            "available_parts": available_parts,
                        }

            else:
                parts = Part.objects.select_related('team').filter(
                    part_type=team.team_type.replace('_TAKIMI', '')
                )
                aircrafts = None
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
        'team_info': team_info if team_info else "Takımsız",
        'ready_aircrafts': ready_aircrafts,  # Üretime hazır uçaklar
    }

    return render(request, 'dashboard.html', context)

#login auth
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

#parça üretimi metodu
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
        # Tarih formatı
        'production_time': part.production_time.strftime('%Y-%m-%d %H:%M:%S'),
        'id': part.id
    }, status=status.HTTP_201_CREATED)


#hava aracı üretimi metodu
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def produce_aircraft(request):
    employee = getattr(request.user, 'employee', None)
    if not employee or not employee.team or employee.team.team_type != 'MONTAJ_TAKIMI':
        return Response({'error': 'Sadece Montaj Takımı uçak üretebilir.'}, status=status.HTTP_403_FORBIDDEN)

    aircraft_type = request.data.get('aircraft_type')

    if not aircraft_type or aircraft_type not in [choice[0] for choice in AIRCRAFT_TYPE_CHOICES]:
        return Response({'error': 'Geçersiz uçak tipi.'}, status=status.HTTP_400_BAD_REQUEST)

    required_parts = ['KANAT', 'GOVDE', 'KUYRUK', 'AVIYONIK']
    missing_parts = []

    #hava aracı üretimi için gerekli koşulların kontrolü
    for part_type in required_parts:
        count_needed = 2 if part_type == 'KANAT' else 1
        available_parts = Part.objects.filter(
            part_type=part_type,
            target_aircraft_type=aircraft_type,
            used=False,
            aircraft__isnull=True
        ).count()
        #parça eksikliğinde bildirmek için kullanılan bölüm
        if available_parts < count_needed:
            missing_parts.append(
                f"{count_needed - available_parts} adet {part_type}")

    if missing_parts:
        return Response({'error': f'Eksik parçalar: {", ".join(missing_parts)}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Montaj takımını kaydet
        new_aircraft = Aircraft.objects.create(aircraft_type=aircraft_type, produced_by=employee.team)

        for part_type in required_parts:
            count_needed = 2 if part_type == 'KANAT' else 1
            parts = Part.objects.filter(
                part_type=part_type,
                target_aircraft_type=aircraft_type,
                used=False,
                aircraft__isnull=True
            )[:count_needed]
            #hava aracı üretiminde parçaların "kullanıldı" döndürmesi
            for part in parts:
                part.aircraft = new_aircraft
                part.used = True
                part.save()

        return Response({'success': f'{new_aircraft.get_aircraft_type_display()} uçağı başarıyla üretildi!'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': f'Uçak üretiminde bir hata oluştu: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#geri dönüşüm metodu
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
