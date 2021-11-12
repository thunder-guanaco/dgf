from django import template
from django.conf import settings
from filer.models.imagemodels import Image

register = template.Library()


@register.simple_tag
def dgf_version():
    return settings.DGF_VERSION


@register.simple_tag
def random_background_img_url():
    background_image = Image.objects.filter(folder__name=settings.BACKGROUND_FOLDER).order_by('?').first()
    return background_image.url if background_image else ''
