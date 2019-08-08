from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r
from django.template.loader import render_to_string

from urbanizze.accounts.forms import AccountForm
from urbanizze.research.models import Research


def register(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)

        if not form.is_valid():
            return render(request, 'register.html',
                          {'form': form})

        user = User.objects.create_user(**form.cleaned_data)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        research = Research(user=user)
        research.save()


        form.full_clean()

        body = render_to_string('subscription_email.txt',
                                form.cleaned_data)

        mail.send_mail('Confirmação de cadastro - URBANIZZE',
                       body,
                       'contato@urbanizze.com.br',
                       ['contato@urbanizze.com.br', form.cleaned_data['email']])

        return HttpResponseRedirect(r('home:home'))

    return render(request, 'register.html',
                  {'form': AccountForm()})
