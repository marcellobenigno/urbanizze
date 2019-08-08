from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.test import TestCase
from urbanizze.map.forms import TerrenoForm
from urbanizze.map.models import Zona


class TerrenoFormTest(TestCase):
    fixtures = ['zonas.json']

    def setUp(self):
        self.credentials = dict(
            username='elliot',
            email='elliot@mrrobot.com',
            password='evilcorp',
        )

        self.user = User.objects.create_user(**self.credentials)
        self.client.login(username='elliot', password='evilcorp')

        self.geom = '''SRID=4326;POLYGON((-34.8357152938843 \
        -7.10025387541908,-34.8346853256226 -7.10131853026714,\
        -34.8339557647705 -7.1010204271581,-34.8357152938843 \
        -7.10025387541908))'''

    def test_form_has_fields(self):
        """Form must have 6 fields"""
        form = TerrenoForm()
        expected = ['edification_type', 'number_pav',
                    'address', 'descricao', 'geom', 'account']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_form_is_valid(self):
        data = dict (
            descricao='Descrição de um terreno.',
            geom=self.geom,
            zona=Zona.objects.get(geom__contains=self.geom).nome,
            edification_type='Comercial',
            number_pav=2,
            account=self.user.id,
        )
        form = TerrenoForm(data)
        self.assertTrue(form.is_valid())

    def test_form_is_valid(self):
        data = dict (
            descricao='Descrição de um terreno.',
            geom=self.geom,
            zona=Zona.objects.get(geom__contains=self.geom).nome,
            edification_type='Comercial',
            number_pav=2,
            account=self.user,
        )
        form = TerrenoForm(data)
        self.assertFalse(form.is_valid())
