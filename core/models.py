from django.db import models
from django.contrib.auth.models import User

PART_TYPE_CHOICES = [
    ('KANAT', 'Kanat'),
    ('GOVDE', 'Gövde'),
    ('KUYRUK', 'Kuyruk'),
    ('AVIYONIK', 'Aviyonik')
]

AIRCRAFT_TYPE_CHOICES = [
    ('TB2', 'TB2'),
    ('TB3', 'TB3'),
    ('AKINCI', 'AKINCI'),
    ('KIZILELMA', 'KIZILELMA')
]

TEAM_TYPE_CHOICES = [
    ('KANAT_TAKIMI', 'Kanat Takımı'),
    ('GOVDE_TAKIMI', 'Gövde Takımı'),
    ('KUYRUK_TAKIMI', 'Kuyruk Takımı'),
    ('AVIYONIK_TAKIMI', 'Aviyonik Takımı'),
    ('MONTAJ_TAKIMI', 'Montaj Takımı')
]

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    team_type = models.CharField(max_length=50, choices=TEAM_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_team_type_display()})"

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Aircraft(models.Model):
    aircraft_type = models.CharField(max_length=50, choices=AIRCRAFT_TYPE_CHOICES)
    production_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_aircraft_type_display()} - {self.id}"

class Part(models.Model):
    part_type = models.CharField(max_length=50, choices=PART_TYPE_CHOICES)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='parts')
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True, blank=True, related_name='parts')
    production_time = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False, help_text="Parça bir uçakta kullanıldı mı?")
    target_aircraft_type = models.CharField(
        max_length=50,
        choices=AIRCRAFT_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text="Hangi uçak tipi için üretildi"
    )

    def __str__(self):
        return f"{self.part_type} - {self.id}"