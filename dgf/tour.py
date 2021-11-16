import logging

logger = logging.getLogger(__name__)

TS_POINTS = {
    1: 20,
    2: 17,
    3: 15,
    4: 10,
    5: 7,
    6: 5,
    7: 4,
    8: 3,
    9: 2,
    10: 1,
}

TS_POINTS_PLUS_BEATEN_PLAYERS = 'TS_POINTS_PLUS_BEATEN_PLAYERS'


def ts_points_with_beaten_players(result):
    position = result.position
    all_results = result.tournament.results.all()
    position_points = TS_POINTS.get(position, 0)
    defeated_players = (all_results.count() - position) / 2
    return position_points + defeated_players


POINT_SYSTEMS = {
    TS_POINTS_PLUS_BEATEN_PLAYERS: ts_points_with_beaten_players,
}


def calculate_points(result):
    tour = result.tournament.tour
    if not tour:
        logger.warning(f'No tour defined for tournament {result.tournament}. Skipping calculating points.')
        return None

    calculate_points_function = POINT_SYSTEMS.get(tour.point_system)
    if calculate_points_function is None:
        logger.error(f'Point system \'{tour.point_system}\' does not exist!')
    return calculate_points_function(result)
