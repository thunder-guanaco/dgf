import logging

from dgf.disc_golf_metrix.tremonia_series import TremoniaSeriesImporter
from dgf.management.base_dgf_command import BaseDgfCommand

logger = logging.getLogger(__name__)


class Command(BaseDgfCommand):
    help = 'Updates tournament information from Tremonia Series (from Disc Golf Metrix)'

    def run(self, *args, **options):
        TremoniaSeriesImporter().update_tournaments()
