import logging

from django.core.management.base import BaseCommand

from dgf import german_tour

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates Friends\' tournament information from German Tour (turniere.discgolf.de)'

    def handle(self, *args, **options):
        logger.info('Fetching German Tour data...')
        german_tour.update_tournaments()
        logger.info('German Tour data has been updated')
