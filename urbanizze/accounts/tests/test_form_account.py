from django.test import TestCase
from urbanizze.accounts.forms import AccountForm


class AccountFormTest(TestCase):
    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = AccountForm()
        expected = ['username', 'email', 'password']
        self.assertSequenceEqual(expected, list(form.fields))
