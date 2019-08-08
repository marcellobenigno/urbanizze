from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError


EDIFICATION = (
    ('Comercial', 'Comercial'),
    ('Residencial', 'Residencial'),
    ('Industrial', 'Industrial'),
    ('Institucional', 'Institucional'),
)


class Setor(models.Model):
    nome = models.CharField('nome', max_length=50)
    geom = models.PolygonField(srid=4326)

    def __str__(self):
        return self.nome


class Zona(models.Model):
    nome = models.CharField('nome', max_length=50)
    geom = models.PolygonField(srid=4326)
    extenso = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Terreno(models.Model):
    descricao = models.CharField('descrição do terreno', max_length=100)
    geom = models.PolygonField(srid=4326)
    zona = models.CharField('zona', max_length=50)
    setor = models.CharField('setor', max_length=50)
    number_pav = models.IntegerField('número de pavimentações')
    edification_type = models.CharField('tipo de edificação', max_length=50,
                                        choices=EDIFICATION)
    account = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao

    def terreno_many_zones_issue(self):
        errors = {}
        if not self.number_pav:
            msg = 'É necessário informar a quantidade de pavimentos do seu terreno.'
            errors.setdefault('geom', []).append(msg)
        if not self.descricao:
            msg = 'É necessário identificar o seu terreno com uma descrição.'
            errors.setdefault('geom', []).append(msg)
        try:
            Zona.objects.get(geom__contains=self.geom)
            Setor.objects.get(geom__contains=self.geom)
        except:
            if self.geom:
                msg1 = '''
                O polígono do terreno que você desenhou está contido em mais de uma zona urbana.
                '''
                msg2 = '''
                Refaça o desenho de forma que o terreno fique contido somente em uma zona.
                '''
                msg3 = '''
                Para auxiliar essa ação ative a camada de visualização das zonas urbanas no mapa de consultas.
                '''
                errors.setdefault('geom', []).append(msg1)
                errors.setdefault('geom', []).append(msg2)
                errors.setdefault('geom', []).append(msg3)
        if errors:
            raise ValidationError(errors)

    def clean(self):
        self.terreno_many_zones_issue()

    def save(self, *args, **kwargs):
        self.zona = Zona.objects.get(geom__contains=self.geom)
        self.setor = Setor.objects.get(geom__contains=self.geom)
        super(Terreno, self).save(*args, **kwargs)


class CodUrbanismo(models.Model):
    zona = models.CharField(max_length=50)
    uso_permitido = models.CharField(max_length=50)
    area_minima = models.CharField(max_length=50)
    frente_minima = models.CharField(max_length=50)
    taxa_ocupacao = models.CharField(max_length=50)
    altura_maxima = models.CharField(max_length=50)
    afast_frente = models.CharField(max_length=50)
    afast_lateral = models.CharField(max_length=50)
    afast_fundos = models.CharField(max_length=50)
