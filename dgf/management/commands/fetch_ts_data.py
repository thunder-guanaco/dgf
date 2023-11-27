import logging

from django.core.management.base import BaseCommand

from dgf.disc_golf_metrix.tremonia_series import TremoniaSeriesImporter
from dgf.management import error_handler

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates tournament information from Tremonia Series (from Disc Golf Metrix)'

    def handle(self, *args, **options):

        try:
            logger.info('Fetching Tremonia Series data...')
            TremoniaSeriesImporter().update_tournaments()
            logger.info('Tremonia Series data has been updated')

        except Exception as e:
            error_handler.handle(self, e)
