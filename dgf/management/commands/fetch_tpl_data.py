import logging

from django.core.management.base import BaseCommand

from dgf.disc_golf_metrix.tremonia_putting_liga import TremoniaPuttingLigaImporter
from dgf.disc_golf_metrix.tremonia_putting_liga_finals import TremoniaPuttingLigaFinalsImporter
from dgf.management import error_handler
from dgf.models import Tour

logger = logging.getLogger(__name__)


def set_positions_from_finals():
    tour = Tour.objects.get(name='1. Tremonia Putting Liga', division='MPO')
    finals = Tour.objects.get(name=f'{tour.name} (finals)', division='MPO')
    for tournament in tour.tournaments.all():
        logger.info(f'  Setting positions for {tournament}')
        final = finals.tournaments.get(name=f'{tournament.name} (final)')
        logger.info(f'  Using final:  {final}')
        for final_position, final_result in enumerate(final.results.order_by('-points'), 1):
            logger.info(f'      Setting position to {final_position} for {final_result.friend}')
            result = tournament.results.get(friend=final_result.friend)
            result.position = final_position
            result.save()
            logger.info('\n')


class Command(BaseCommand):
    help = 'Updates tournament information from Tremonia Putting Liga (from Disc Golf Metrix)'

    def run(self, what, text):
        logger.info(f'{text}...')
        what()
        logger.info(f'{text} DONE')

    def handle(self, *args, **options):

        try:
            self.run(TremoniaPuttingLigaImporter().update_tournaments, 'Fetch TPL data')
            self.run(TremoniaPuttingLigaFinalsImporter().update_tournaments, 'Fetch TPL Finals data')
            self.run(set_positions_from_finals, 'Set positions from TPL Finals')

        except Exception as e:
            error_handler.handle(self, e)
