import csv
import logging
from decimal import Decimal

import requests
from django.conf import settings

from .models import Friend, Disc
from .pdga import PdgaApi

logger = logging.getLogger(__name__)


def update_tournaments(pdga_service):
    for friend in Friend.objects.all():
        if friend.pdga_number:
            statistics = pdga_service.query_player_statistics(pdga_number=friend.pdga_number)

            money_earned = 0
            tournaments = 0
            for yearly_stats in statistics['players']:
                try:
                    money_earned += Decimal(yearly_stats['prize'])
                except KeyError:
                    # not all years have to have prizes
                    pass
                try:
                    tournaments += int(yearly_stats['tournaments'])
                except KeyError:
                    # maybe not all years have to have tournaments
                    pass

            friend.total_earnings = money_earned
            friend.total_tournaments = tournaments
            friend.save()


def update_ratings(pdga_service):
    for friend in Friend.objects.all():
        if friend.pdga_number:
            pdga_friend_response = pdga_service.query_player(pdga_number=friend.pdga_number)
            rating = pdga_friend_response['players'][0]['rating']
            if rating:
                friend.rating = int(rating)
                friend.save()
                logger.info('{} has now rating: {}'.format(friend.username, friend.rating))
            else:
                logger.info(
                    '{} had no rating in the PDGA yet, possible reasons: membership outdated or new member'.format(
                        friend.username))


def fetch_pdga_data():
    pdga_service = PdgaApi()
    update_ratings(pdga_service)
    update_tournaments(pdga_service)


def update_approved_discs(approved_discs):
    loaded_discs = csv.DictReader(approved_discs, delimiter=',')
    stored_discs = [x for x in Disc.objects.all().values_list('mold', flat=True)]

    for disc in loaded_discs:
        if disc['Disc Model'] not in stored_discs:
            new_disc = Disc(mold=disc['Disc Model'],
                            manufacturer=disc['Manufacturer / Distributor'])
            new_disc.save()


def update_approved_discs_cron():
    # download CSV from the PDGA
    response = requests.get(settings.APPROVED_DISCS_URL)
    csv_list = str(response.content, 'utf-8').replace('\r\n', '\n').split('\n')
    update_approved_discs(csv_list)
