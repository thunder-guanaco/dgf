from django.db.models.signals import post_save
from django.dispatch import receiver

from .cronjobs import fetch_pdga_data
from .models import Friend


@receiver(post_save, sender=Friend)
def post_save_handler(sender, **kwargs):
    fetch_pdga_data()
