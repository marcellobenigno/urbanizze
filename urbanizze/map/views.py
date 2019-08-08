import json

from decouple import config

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from djgeojson.views import GeoJSONLayerView

from geopy.geocoders import GoogleV3

from urbanizze.map.forms import TerrenoForm
from urbanizze.map.models import Terreno, Zona, Setor, CodUrbanismo


class ZonasGeoJson(GeoJSONLayerView):
    model = Zona
    properties = ('nome',)


class SetorGeoJson(GeoJSONLayerView):
    model = Setor
    properties = ('nome',)


geojson_zonas = ZonasGeoJson.as_view()
geojson_setor = SetorGeoJson.as_view()


def home(request):
    return render(request, 'index.html')


@login_required()
def list(request):
    terrenos = Terreno.objects.all()
    users = User.objects.all()

    for terreno in terrenos:
        for user in users:
            if terreno.account_id == user.id:
                terreno.username = user.username

    return render(request, 'list.html', {'terrenos': terrenos})


@login_required()
def create(request):
    form = TerrenoForm(request.POST or None, initial={'account': request.user})

    if form.is_valid():
        terreno = form.save()
        return redirect('home:result', terreno.pk)

    context = {
        'form': form,
        'x': settings.MAP_CENTER_X,
        'y': settings.MAP_CENTER_Y,
        'zoom_init': settings.ZOOM_INIT,
    }

    return render(request, 'create.html', context)


# TODO ~ extract this method
def result(request, pk):
    try:
        terreno = Terreno.objects.get(pk=pk)
    except Terreno.DoesNotExist:
        raise Http404

    cod_result = CodUrbanismo.objects.filter(zona=terreno.zona)
    # obj_zona = Zona.objects.get(nome=terreno.zona)
    obj_zona = Zona.objects.get(geom__contains=terreno.geom)

    if len(cod_result) == 0:
        return render(request, 'no_data.html')

    zona = terreno.zona
    zona_extenso = obj_zona.extenso
    cidade = 'João Pessoa'
    tipo_edificacao = terreno.edification_type
    numero_pavimento = terreno.number_pav
    uso_permitido = [x.uso_permitido for x in cod_result]

    if tipo_edificacao == 'Comercial':
        uso_permitido = [x for x in uso_permitido if 'Comércio' in x]
    else:
        uso_permitido = [x for x in uso_permitido if tipo_edificacao in x]

    numero_uso_permitido = len(uso_permitido)
    numero_pavimento_permitido = True

    if zona == 'ZR-1':
        if tipo_edificacao != 'Residencial':
            return render(request, 'no_data.html')
    elif zona == 'ZT-2':
        if tipo_edificacao != 'Comercial':
            return render(request, 'no_data.html')
    elif zona == 'ZA-3':
        if tipo_edificacao == 'Industrial' or tipo_edificacao == 'Institucional':
            return render(request, 'no_data.html')

    if zona == 'ZR-1' or zona == 'ZT-2':
        if numero_pavimento > 4:
            return render(request, 'no_data.html')
    elif zona == 'ZA-3':
        if numero_pavimento >= 3 and tipo_edificacao == 'Residencial':
            numero_pavimento_permitido = False

    context = {
        'terreno': terreno,
        'zona': zona,
        'zona_extenso': zona_extenso,
        'cidade': cidade,
        'tipo_edificacao': tipo_edificacao,
        'numero_pavimento': numero_pavimento,
        'uso_permitido': uso_permitido,
        'numero_uso_permitido': numero_uso_permitido,
        'cod_result': cod_result,
        'numero_pavimento_permitido': numero_pavimento_permitido,
    }

    return render(request, 'result.html', context)


def reverse_geocoding(request):
    if request.is_ajax() and request.POST:
        geolocator = GoogleV3(api_key=config('GOOGLE_MAPS_API_KEY'))
        address = request.POST.get('address')
        try:
            location = geolocator.geocode("{}".format(address))

            geodata = {'address': location.address,
                       'latitude': location.latitude,
                       'longitude': location.longitude}

            return HttpResponse(json.dumps(geodata),
                                content_type='application/json')
        except:
            raise Http404
    else:
        raise Http404


@login_required()
def export(request, pk):
    import os

    _id = pk
    path = settings.MEDIA_ROOT + '/'
    host = "-h localhost -u urbanizze -P {} {}"
    host = host.format(config('DATABASE_PASSWORD'),
                       config('DATABASE_USERNAME'))
    sql = 'SELECT geom FROM map_terreno WHERE id = {}'.format(_id)

    # create shape file
    os.system('pgsql2shp -f {}terreno_{} {} "{}"'
              .format(path, _id, host, sql))

    # create dxf file
    os.system('ogr2ogr -f DXF {0}terreno_{1}.dxf {0}terreno_{1}.shp'
              .format(path, _id))

    return render(request, 'export.html', {'pk': pk})
