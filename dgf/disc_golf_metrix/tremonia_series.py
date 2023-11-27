import logging

from dgf.disc_golf_metrix.disc_golf_metrix import DiscGolfMetrixImporter
from dgf.models import Tournament

logger = logging.getLogger(__name__)

TREMONIA_SERIES_ROOT_ID = '715021'


class TremoniaSeriesImporter(DiscGolfMetrixImporter):

    @property
    def root_id(self):
        return TREMONIA_SERIES_ROOT_ID

    @property
    def point_system(self):
        return Tournament.TS_POINTS_WITH_BEATEN_PLAYERS

    @property
    def divisions(self):
        return {
            'Open': 'MPO',
            'Amateur': 'MA4',
        }

    def extract_name(self, dgm_tournament):
        return dgm_tournament['Name'].split(' &rarr; ')[-1]

    def generate_tours(self, tournament):
        return [
            # default tour containing all Tremonia Series
            ('Ewige Tabelle', 10000),

            # tournament year's tour (best 7 tournaments count towards year's leaderboard)
            (f'Tremonia Series {tournament.begin.year}', 7)
        ]
