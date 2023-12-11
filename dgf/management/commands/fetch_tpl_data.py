import logging

from dgf.disc_golf_metrix.tremonia_putting_liga import TremoniaPuttingLigaImporter
from dgf.disc_golf_metrix.tremonia_putting_liga_finals import TremoniaPuttingLigaFinalsImporter
from dgf.management.base_dgf_command import BaseDgfCommand
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
        logger.info('')


class Command(BaseDgfCommand):
    help = 'Updates tournament information from Tremonia Putting Liga (from Disc Golf Metrix)'

    def run_with_logs(self, what, text):
        logger.info(f'{text}...')
        what()
        logger.info(f'{text} DONE')

    def run(self, *args, **options):
        self.run_with_logs(TremoniaPuttingLigaImporter().update_tournaments, 'Fetch TPL data')
        self.run_with_logs(TremoniaPuttingLigaFinalsImporter().update_tournaments, 'Fetch TPL Finals data')
        self.run_with_logs(set_positions_from_finals, 'Set positions from TPL Finals')
