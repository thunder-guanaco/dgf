import logging

from dgf import german_tour
from dgf.management.base_dgf_command import BaseDgfCommand

logger = logging.getLogger(__name__)


class Command(BaseDgfCommand):
    help = 'Updates Friends\' tournament information from German Tour (turniere.discgolf.de)'

    def run(self, *args, **options):
        german_tour.update_all_tournaments()
