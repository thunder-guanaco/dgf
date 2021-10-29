import logging

from django.core.management.base import BaseCommand

from dgf import tremonia_series

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates tournament information from Tremonia Series (from Disc Golf Metrix)'

    def handle(self, *args, **options):
        logger.info('Fetching Tremonia Series data...')
        tremonia_series.update_tournaments()
        logger.info('Tremonia Series data has been updated')
