from django import forms


class AccountForm(forms.Form):
    username = forms.CharField(label='Usuário')
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
