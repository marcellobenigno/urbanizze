from django.contrib.auth.models import User
from django.test import TestCase
from urbanizze.map.models import Terreno, Zona, Setor


class TerrenoModel(TestCase):
    fixtures = ['zonas.json', 'setor.json']

    def setUp(self):
        self.credentials = dict(
            username='elliot',
            email='elliot@mrrobot.com',
            password='evilcorp',
        )

        self.user = User.objects.create_user(**self.credentials)

        geom = '''SRID=4326;POLYGON((-34.8357152938843 \
        -7.10025387541908,-34.8346853256226 -7.10131853026714,\
        -34.8339557647705 -7.1010204271581,-34.8357152938843 \
        -7.10025387541908))'''

        self.obj = Terreno(
            edification_type='Comercial',
            number_pav=4,
            descricao='Descrição de um terreno.',
            geom=geom,
            zona=Zona.objects.get(geom__contains=geom),
            setor=Setor.objects.get(geom__contains=geom),
            account=self.user,
        )

        self.obj.save()

    def test_create(self):
        self.assertTrue(Terreno.objects.exists())

    def test_str(self):
        self.assertTrue('Descrição de um terreno.', str(self.obj))
