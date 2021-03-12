import logging

from django.core.management.base import BaseCommand

from dgf.models import Friend
from dgf.pdga import PdgaApi

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates Friend\'s rating and tournament information'

    def handle(self, *args, **options):
        logger.info('Fetching PDGA data...')

        pdga_api = PdgaApi()
        for friend in Friend.objects.all():
            pdga_api.update_friend_rating(friend)
            pdga_api.update_friend_tournament(friend)
            friend.save()

        logger.info('PDGA data has been updated')
