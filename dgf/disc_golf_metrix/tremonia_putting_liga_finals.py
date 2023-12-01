import logging

from dgf.disc_golf_metrix.tremonia_putting_liga import TremoniaPuttingLigaImporter

logger = logging.getLogger(__name__)

ROOT_ID = '2804918'


class TremoniaPuttingLigaFinalsImporter(TremoniaPuttingLigaImporter):
    root_id = ROOT_ID
    unwanted_tournaments_regex = r'^Tremonia Putting Liga &rarr; Finale-Runden &rarr; (\[DELETED])'

    def extract_name(self, dgm_tournament):
        split_name = dgm_tournament['Name'].split(' &rarr; ')
        return f'{split_name[2]} {split_name[0]} (final)'

    def generate_tours(self, tournament):
        return [
            # this tour won't be displayed on the web
            ('1. Tremonia Putting Liga (finals)', 10000)
        ]

    def get_results(self, dgm_tournament):
        return dgm_tournament['Results']

    def get_tpl_points(self, dgm_result):
        station_putts = [int(station_result['Result']) if 'Result' in station_result else 0
                         for station_result in dgm_result['PlayerResults']]

        return self.calculate_round_score(station_putts)
