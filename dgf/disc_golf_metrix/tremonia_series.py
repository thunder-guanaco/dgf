import logging

from dgf.disc_golf_metrix import disc_golf_metrix
from dgf.models import Tournament

logger = logging.getLogger(__name__)

TREMONIA_SERIES_ROOT_ID = '715021'

TS_DIVISIONS = {
    'Open': 'MPO',
    'Amateur': 'MA4',
}


def generate_tours(tournament):
    return [
        # default tour containing all Tremonia Series
        ('Ewige Tabelle', 10000),

        # tournament year's tour (best 7 tournaments count towards year's leaderboard)
        (f'Tremonia Series {tournament.begin.year}', 7)
    ]


def update_tournaments():
    disc_golf_metrix.update_tournaments(TREMONIA_SERIES_ROOT_ID,
                                        point_system=Tournament.TS_POINTS_WITH_BEATEN_PLAYERS,
                                        divisions=TS_DIVISIONS,
                                        tour_generator=generate_tours)
