import logging

from django.core.management.base import BaseCommand

from dgf.disc_golf_metrix.tremonia_putting_liga import TremoniaPuttingLigaImporter
from dgf.management import error_handler

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates tournament information from Tremonia Putting Liga (from Disc Golf Metrix)'

    def handle(self, *args, **options):

        try:
            logger.info('Fetching Tremonia Putting Liga data...')
            TremoniaPuttingLigaImporter().update_tournaments()
            logger.info('Tremonia Putting Liga data has been updated')

        except Exception as e:
            error_handler.handle(self, e)
