from django.contrib.auth.models import User
from django.test import TestCase


class AccountModelTest(TestCase):
    def setUp(self):
        self.credentials = dict(
            username='elliot',
            email='elliot@mrrobot.com',
            password='evilcorp',
        )

        self.user = User.objects.create_user(**self.credentials)

    def test_create(self):
        self.assertTrue(User.objects.exists())

    def test_username(self):
        self.assertEqual('elliot', self.user.username)

    def test_str(self):
        self.assertEqual('elliot', str(self.user))
