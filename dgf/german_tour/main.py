import logging
from datetime import date

from dgf.german_tour.attendance import update_tournament_attendance
from dgf.german_tour.common import get_all_tournaments_from_list_page, get_all_tournaments_from_ratings_page, \
    parse_tournament_from_details_page, delete_tournament, add_or_update_tournament
from dgf.german_tour.results import update_tournament_results

logger = logging.getLogger(__name__)


def update_all_tournaments():
    ids_from_list_page = get_all_tournaments_from_list_page()
    ids_from_ratings_page = get_all_tournaments_from_ratings_page()
    all_tournament_ids = ids_from_list_page | ids_from_ratings_page
    logger.info(f'{len(all_tournament_ids)} tournaments to update')

    for tournament_id in all_tournament_ids:

        logger.info('\n-------------------------------------------')
        gt_tournament = parse_tournament_from_details_page(tournament_id)

        if gt_tournament['name'].startswith('Tremonia Series #'):
            logger.info(f'Ignoring tournament: {gt_tournament["name"]}. '
                        f'Tremonia Series tournaments are handled separately')

        elif gt_tournament['canceled']:
            delete_tournament(gt_tournament)

        else:
            tournament = add_or_update_tournament(gt_tournament)

            # tournament is either not played yet or still in play
            if tournament.end >= date.today():
                update_tournament_attendance(tournament)

            # tournament was already played
            else:
                update_tournament_results(tournament)
