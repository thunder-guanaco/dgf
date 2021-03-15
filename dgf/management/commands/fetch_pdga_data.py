import logging

from django.core.management.base import BaseCommand

from dgf.models import Friend
from dgf.pdga import PdgaApi, PdgaCrawler

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates Friend\'s rating and tournament information'

    def handle(self, *args, **options):
        logger.info('Fetching PDGA data...')

        pdga_api = PdgaApi()
        pdga_crawler = PdgaCrawler()

        for friend in Friend.objects.all():
            pdga_api.update_friend_rating(friend)
            pdga_api.update_friend_tournament_statistics(friend)
            pdga_crawler.update_friend_tournaments(friend)

        pdga_api.logout()
        pdga_crawler.quit()

        logger.info('PDGA data has been updated')
