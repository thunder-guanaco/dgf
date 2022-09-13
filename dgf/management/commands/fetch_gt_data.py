import logging

from django.core.management.base import BaseCommand

from dgf.german_tour.attendance import update_all_tournaments_attendance
from dgf.german_tour.results import update_all_tournaments_results
from dgf.management import error_handler

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates Friends\' tournament information from German Tour (turniere.discgolf.de)'

    def handle(self, *args, **options):

        try:
            logger.info('Fetching German Tour data...')
            update_all_tournaments_attendance()
            update_all_tournaments_results()
            logger.info('German Tour data has been updated')

        except Exception as e:
            error_handler.handle(self, e)
