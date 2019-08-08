from django.conf import settings


def map_media(request):
    return {'MEDIA_URL': settings.MEDIA_URL}
