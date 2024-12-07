"""Unit Test
Bu Test Ne Yapar?
setUp metodu, her test çalıştırılmadan önce bir Team örneği oluşturur.
test_create_part, bir Part nesnesinin doğru bir şekilde oluşturulup oluşturulmadığını test eder.
test_part_str_representation, Part modelinin __str__ metodu varsa, doğru bir string temsiline sahip olup olmadığını kontrol eder.
"""


from django.test import TestCase
from core.models import Team, Part

class PartModelTestCase(TestCase):
    def setUp(self):
        # Test için bir takım oluştur
        self.team = Team.objects.create(name="KANAT_TAKIMI", team_type="KANAT_TAKIMI")
    
    def test_create_part(self):
        # Test için bir parça oluştur
        part = Part.objects.create(
            part_type="KANAT",
            team=self.team,
            target_aircraft_type="SAVAS_UCAGI",
            used=False
        )

        # Parça oluşturma doğrulama
        self.assertEqual(part.part_type, "KANAT")
        self.assertEqual(part.team.name, "KANAT_TAKIMI")
        self.assertEqual(part.target_aircraft_type, "SAVAS_UCAGI")
        self.assertFalse(part.used)

    def test_part_str_representation(self):
        # Parçanın string temsilini test et
        part = Part.objects.create(
            part_type="KANAT",
            team=self.team,
            target_aircraft_type="SAVAS_UCAGI",
            used=False
        )

        # String temsili kontrol et
        self.assertEqual(str(part), f"{part.part_type} - {part.target_aircraft_type}")
