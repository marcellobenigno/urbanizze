from django.test import TestCase
from urbanizze.map.models import Zona


class ZonaModel(TestCase):
    def setUp(self):
        self.obj = Zona(
            nome='Nome Zona',
            geom='''SRID=4326;POLYGON((-34.8318314552307 \
            -7.11966214592647,-34.8315739631653 -7.12057771055656,\
            -34.8307907581329 -7.12039672699553,-34.8310106992722 \
            -7.1196195614806,-34.8318314552307 -7.11966214592647))''',
        )

        self.obj.save()

    def test_create(self):
        self.assertTrue(Zona.objects.exists())

    def test_str(self):
        self.assertTrue('Nome Zona', str(self.obj))
