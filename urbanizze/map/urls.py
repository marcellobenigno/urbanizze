from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from .views import home, create, list
from urbanizze.research.views import research
from .views import geojson_zonas, geojson_setor
from .views import reverse_geocoding, export, result

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^pesquisa/$', research, name='research'),
    url(r'^cadastro/$', create, name='cadastro'),
    url(r'^terrenos/$', list, name='terrenos'),
    url(r'^zonas.geojson/$', geojson_zonas, name='geojson_zonas'),
    url(r'^setor.geojson/$', geojson_setor, name='geojson_setor'),
    url(r'^ajax/geocoding/$', reverse_geocoding, name='reverse_geocoding'),
    url(r'^(?P<pk>\d+)/export/$', export, name='export'),
    url(r'^resultado/(\d+)/$', result, name='result'),
]
