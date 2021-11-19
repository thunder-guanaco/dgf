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


def ts_points_with_beaten_players(result):
    position = result.position
    all_results = result.tournament.results.all()
    position_points = TS_POINTS.get(position, 0)
    defeated_players_points = (all_results.count() - position) // 2
    return position_points + defeated_players_points


def calculate_points(result):
    point_system = result.tournament.point_system
    calculate_points_function = globals().get(point_system)
    if calculate_points_function is None:
        logger.error(f'Point system \'{point_system}\' does not exist! '
                     f'Please define a function with that name on tour.py')
        return None

    return calculate_points_function(result)
