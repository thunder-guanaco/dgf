import csv
import logging

import requests
from django.conf import settings

from .models import Friend, Disc
from .pdga import PdgaApi

logger = logging.getLogger(__name__)


def update_tournaments(pdga_service):
    for friend in Friend.objects.all():
        pdga_service.update_friend_tournament(friend)
        friend.save()


def update_ratings(pdga_service):
    for friend in Friend.objects.all():
        pdga_service.update_friend_rating(friend)
        friend.save()


def fetch_pdga_data():
    pdga_service = PdgaApi()
    update_ratings(pdga_service)
    update_tournaments(pdga_service)


def update_approved_discs(approved_discs):
    loaded_discs = csv.DictReader(approved_discs, delimiter=',')
    stored_discs = [x for x in Disc.objects.all().values_list('mold', flat=True)]

    for disc in loaded_discs:
        if disc['Disc Model'] not in stored_discs:
            Disc.objects.get_or_create(mold=disc['Disc Model'],
                                       defaults={'manufacturer': disc['Manufacturer / Distributor']})


def update_approved_discs_cron():
    # download CSV from the PDGA
    response = requests.get(settings.APPROVED_DISCS_URL)
    csv_list = str(response.content, 'utf-8').replace('\r\n', '\n').split('\n')
    update_approved_discs(csv_list)
