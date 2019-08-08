import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.http import Http404, HttpResponse
from django.shortcuts import resolve_url as r
from django.test import TestCase
from urbanizze.map.forms import TerrenoForm
from urbanizze.map.models import Zona, Terreno, Setor


class TerrenoCreate(TestCase):
    def setUp(self):
        self.credentials = dict(username='elliot', password='mrrobot')
        self.user = User.objects.create_user(**self.credentials)
        self.login = self.client.login(**self.credentials)
        self.resp = self.client.get(r('home:cadastro'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'create.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 2),
                ('type="submit"', 1),
                ('class="btn btn-primary"', 1),
                )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_forms(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, TerrenoForm)


class TerrenoPost(TestCase):
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

        self.data = dict (
            descricao='Descrição de um terreno.',
            geom=geom,
            zona=Zona.objects.get(geom__contains=geom).nome,
            setor=Setor.objects.get(geom__contains=geom).nome,
            edification_type='Comercial',
            number_pav=2,
            account=self.user.id,
        )

        self.resp = self.client.post(r('home:cadastro'), self.data)

    def test_post(self):
        """Valid POST should redirect to /resultado/{pk}/"""
        pk = int(self.resp.url.split('/')[-2])
        self.assertRedirects(self.resp, r('home:result', pk))


class TerrenoPostInvalid(TestCase):
    fixtures = ['zonas.json', 'setor.json']

    def setUp(self):
        self.credentials = dict(
            username='elliot',
            email='elliot@mrrobot.com',
            password='evilcorp',
        )

        self.user = User.objects.create_user(**self.credentials)
        self.client.login(username='elliot', password='evilcorp')

        self.data = dict(
            descricao='',
            zona=Zona.objects.get(pk=2).nome,
            geom='',
            account=self.user,
            edification_type='Comercial',
            number_pav=4,
        )

        self.resp = self.client.post(r('home:cadastro'), self.data)

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'create.html')

    def test_has_forms(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, TerrenoForm)

    def test_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_terreno(self):
        self.assertFalse(Terreno.objects.exists())


class TerrenoAjaxSearchAddress(TestCase):
    def setUp(self):
        data = {'address': 'epitácio pessoa, 4200'}
        self.resp = self.client.post('/ajax/geocoding/', data,
                                     HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_post(self):
        """Valid ajax POST should return 200"""
        self.assertEqual(self.resp.status_code, 200)

    def test_response_has_address_data(self):
        """Response must contain address, latitude and longitude"""
        keys = ('latitude', 'longitude', 'address')
        for key in keys:
            with self.subTest():
                self.assertContains(self.resp, key)
