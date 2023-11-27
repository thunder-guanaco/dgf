import logging

from dgf.disc_golf_metrix.disc_golf_metrix import DiscGolfMetrixImporter
from dgf.models import Tournament, Result

logger = logging.getLogger(__name__)

TREMONIA_PUTTING_LIGA_ROOT_ID = '2766342'
AMOUNT_OF_ROUNDS = 4
SCORE_MULTIPLICATORS = [1, 2, 3, 4, 5] * AMOUNT_OF_ROUNDS
WHATEVER = 999


def get_tpl_points(dgm_result):
    station_putts = [int(station_result['Result']) if 'Result' in station_result else 0
                     for round_results in dgm_result['AllPlayerResults']
                     for station_result in round_results]

    scores = [putts * multiplicator + (1 if putts == 3 else 0)
              for putts, multiplicator in zip(station_putts, SCORE_MULTIPLICATORS)]

    return sum(scores)


class TremoniaPuttingLigaImporter(DiscGolfMetrixImporter):

    @property
    def unwanted_tournaments_regex(self):
        return r'^Tremonia Putting Liga &rarr; (\[DELETED]|Finale|Minispiele)'

    @property
    def root_id(self):
        return TREMONIA_PUTTING_LIGA_ROOT_ID

    @property
    def point_system(self):
        return Tournament.KEEP_POINTS_FROM_IMPORT

    @property
    def divisions(self):
        return {
            'Open': 'MPO',
        }

    def extract_name(self, dgm_tournament):
        return ' '.join(reversed(dgm_tournament['Name'].split(' &rarr; ')))

    def generate_tours(self, tournament):
        return [
            # (best 6 tournaments count towards the leaderboard)
            ('1. Tremonia Putting Liga', 6)
        ]

    def get_position(self, dgm_result):
        return WHATEVER  # in the end, it doesn't even matter: we only count points

    def get_results(self, dgm_tournament):
        if not dgm_tournament['HasSubcompetitions']:
            return []

        results = dict()
        for sub_competition in dgm_tournament['SubCompetitions']:
            for result in sub_competition['Results']:
                user_id = result['UserID']
                if user_id in results:
                    results[user_id]['AllPlayerResults'].append(result['PlayerResults'])
                else:
                    results[user_id] = {
                        'UserID': result['UserID'],
                        'Name': result['Name'],
                        'AllPlayerResults': [result['PlayerResults']],  # a list to add more later
                    }
        return results.values()

    def create_result(self, dgm_result, division, friend, tournament):
        return Result.objects.create(tournament=tournament,
                                     friend=friend,
                                     position=self.get_position(dgm_result),
                                     points=get_tpl_points(dgm_result),
                                     division=division)
