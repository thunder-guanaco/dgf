from django import template
from django.conf import settings
from filer.models.imagemodels import Image

register = template.Library()


@register.simple_tag
def dgf_version():
    return settings.DGF_VERSION


@register.filter
def is_reviewer(user):
    if user is None:
        return False
    return user.groups.filter(name=settings.REVIEWER_GROUP).exists()


@register.simple_tag
def random_background_img_url(friend):
    all_images = Image.objects.filter(folder__name=settings.BACKGROUND_FOLDER)

    if friend:
        all_images = all_images.filter(original_filename__icontains=friend.username)

    background_image = all_images.order_by('?').first()
    return background_image.url if background_image else ''
