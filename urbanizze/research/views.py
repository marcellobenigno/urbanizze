from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r

from urbanizze.research.models import Research
from urbanizze.map.views import create


def research(request):
    if request.method == 'POST':
        if 'research-approved' in request.POST:
            try:
                research = Research.objects.get(user=request.user)
                research.accepted = True
                research.save()
            except:
                try:
                    if request.user:
                        res = Research(user=request.user, accepted=True)
                        res.save()
                except:
                    pass
            return HttpResponseRedirect(r('home:cadastro'))
        else:
            return HttpResponseRedirect(r('home:home'))
    else:
        try:
            research = Research.objects.get(user=request.user)
        except:
            return render(request, 'research.html')
        if not research.accepted:
            return render(request, 'research.html')
        else:
            return HttpResponseRedirect(r('home:cadastro'))
