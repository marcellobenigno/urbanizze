import os

from django.contrib.gis.utils import LayerMapping

from urbanizze.map.models import ZonaCreator

zonacreator_mapping = {
    'name' : 'Name',
    'descriptio' : 'descriptio',
    'timestamp' : 'timestamp',
    'begin' : 'begin',
    'end' : 'end',
    'altitudemo' : 'altitudeMo',
    'tessellate' : 'tessellate',
    'extrude' : 'extrude',
    'visibility' : 'visibility',
    'draworder' : 'drawOrder',
    'icon' : 'icon',
    'geom' : 'POLYGON25D',
}

shape_path = 'urbanizze/map/data/ARQUIVOS_SHP_F/ZT2_SIRGAS_2000_UTM_25S.shp'
zonacreator_shp = os.path.abspath(os.path.join(shape_path))


def run(verbose=True):
    lm1 = LayerMapping(ZonaCreator, zonacreator_shp, zonacreator_mapping)
    lm1.save(strict=True, verbose=verbose)
