import logging

from django.core.management.base import BaseCommand

from dgf import german_tour
from dgf.management import error_handler

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates Friends\' tournament information from German Tour (turniere.discgolf.de)'

    def handle(self, *args, **options):

        try:
            logger.info('Fetching German Tour data...')
            german_tour.update_tournament_attendance()
            german_tour.update_turniere_discgolf_de_tournament_results()
            logger.info('German Tour data has been updated')

        except Exception as e:
            error_handler.handle(self, e)
