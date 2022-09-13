import logging

from django.core.management.base import BaseCommand

from dgf import pdga
from dgf.management import error_handler
from dgf.models import Friend
from dgf.pdga import PdgaApi

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates Friend\'s rating and tournament information'

    def handle_friend(self, pdga_api, friend):

        try:

            pdga_api.update_friend_rating(friend)
            pdga_api.update_friend_tournament_statistics(friend)
            pdga.update_friend_tournaments(friend, pdga_api)

        except Exception as e:
            error_handler.handle(self, e, friend)

    def handle(self, *args, **options):

        try:

            logger.info('Fetching PDGA data...')
            pdga_api = PdgaApi()

            for friend in Friend.objects.all():
                self.handle_friend(pdga_api, friend)

            pdga_api.logout()
            logger.info('PDGA data has been updated')

        except Exception as e:
            error_handler.handle(self, e)
