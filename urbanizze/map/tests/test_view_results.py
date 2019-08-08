from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase
from urbanizze.map.models import Terreno, Zona, Setor


class ResultGet(TestCase):
    fixtures = ['zonas.json', 'setor.json']

    def setUp(self):
        self.credentials = dict(
            username='elliot',
            email='elliot@mrrobot.com',
            password='evilcorp',
        )

        self.user = User.objects.create_user(**self.credentials)
        self.client.login(username='elliot', password='evilcorp')

        geom = '''SRID=4326;POLYGON((-34.8357152938843 \
        -7.10025387541908,-34.8346853256226 -7.10131853026714,\
        -34.8339557647705 -7.1010204271581,-34.8357152938843 \
        -7.10025387541908))'''

        self.obj = Terreno.objects.create(
            descricao='Descrição de um terreno.',
            geom=geom,
            zona=Zona.objects.get(geom__contains=geom).nome,
            setor=Setor.objects.get(geom__contains=geom).nome,
            edification_type='Residencial',
            number_pav=2,
            account=self.user,
        )

        self.resp = self.client.get(r('home:result', self.obj.pk))

    def test_get(self):
        """GET /resultado/{terreno_id} must resturn status code 200"""
        self.assertEqual(200, self.resp.status_code)

    # def test_template(self):
    #     self.assertTemplateUsed(self.resp, 'result.html')

    # def test_context(self):
    #     terreno = self.resp.context['terreno']
    #     self.assertIsInstance(terreno, Terreno)

    # def test_html(self):
    #     contents = (self.obj.zona, self.obj.number_pav, self.obj.edification_type)

    #     with self.subTest():
    #         for expected in contents:
    #             self.assertContains(self.resp, expected)


class ResultNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get(r('home:result', 0))
        self.assertEqual(404, resp.status_code)
