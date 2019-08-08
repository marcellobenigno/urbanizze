from django.test import TestCase
from urbanizze.map.models import CodUrbanismo


class CodUrbanismoModel(TestCase):
    def setUp(self):
        self.obj = CodUrbanismo(
            zona='ZA-3',
            uso_permitido='Residencial 5',
            area_minima='600',
            frente_minima='20',
            taxa_ocupacao='30',
            altura_maxima='4',
            afast_frente='5',
            afast_lateral='4',
            afast_fundos='4',
        )

        self.obj.save()

    def test_create(self):
        self.assertTrue(CodUrbanismo.objects.exists())
