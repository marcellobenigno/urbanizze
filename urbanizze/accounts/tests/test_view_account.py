from django.contrib.auth.models import User
from django.core import mail
from django.shortcuts import resolve_url as r
from django.test import TestCase
from urbanizze.accounts.forms import AccountForm


class AccountLoginLogout(TestCase):
    def setUp(self):
        self.credentials = dict(username='elliot', password='mrrobot')
        self.user = User.objects.create_user(**self.credentials)
        self.login = self.client.login(**self.credentials)
        self.resp = self.client.get(r('accounts:login'))

    def test_login_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_logout_get(self):
        self.resp = self.client.get(r('accounts:logout'))
        self.assertEqual(302, self.resp.status_code)

    def test_terreno_create_must_redirect_if_not_logged(self):
        """Must redirect to login if user not authenticated"""
        self.client.logout()
        response = self.client.get(r('home:cadastro'))
        self.assertEqual(302, response.status_code)

    def test_terreno_create_must_return_200_if_logged(self):
        """Must redirect to login if user not authenticated"""
        response = self.client.get(r('home:cadastro'))
        self.assertEqual(200, response.status_code)

    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 3),
                ('type="text"', 1),
                ('type="password"', 1),
                ('type="submit"', 1),
                ('class="btn btn-primary"', 2),
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')


class AccountRegister(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('accounts:register'))
    def test_get(self):
        """Get /register/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use register.html"""
        self.assertTemplateUsed(self.resp, 'register.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 4),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="password"', 1),
                ('type="submit"', 1),
                ('class="btn btn-primary"', 1),
        )

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_hast_form(self):
        """Context must have accounts form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, AccountForm)


class AccountRegisterPostValid(TestCase):
    def setUp(self):
        credentials = dict(
            username='elliot',
            email='elliot@mrrobot.com',
            password='evilcorp',
        )

        self.resp = self.client.post(r('accounts:register'), credentials)

    def test_post(self):
        """Valid POST should redirect to /map/"""
        self.assertRedirects(self.resp, r('home:home'))

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de cadastro - URBANIZZE'

        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@urbanizze.com.br'

        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@urbanizze.com.br', 'elliot@mrrobot.com']

        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('elliot', email.body)


class AccountRegisterPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post(r('accounts:register'), {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'register.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 4),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="password"', 1),
                ('type="submit"', 1),
                ('class="btn btn-primary"', 1),
        )

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_hast_form(self):
        """Context must have accounts form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, AccountForm)
