from django.shortcuts import resolve_url as r
from django.test import TestCase


class HomeGet(TestCase):
    def setUp(self):
        self.response = self.client.get(r('home:home'))

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'index.html')

    def test_html(self):
        tags = (
            'role="button"',
        )
        for expected in tags:
            with self.subTest():
                self.assertContains(self.response, expected)


class PesquisaGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/pesquisa/')

    def test_get(self):
        """GET /pesquisa/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use research.html"""
        self.assertTemplateUsed(self.response, 'research.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (('class="btn btn-primary btn-lg"', 2),)

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)
