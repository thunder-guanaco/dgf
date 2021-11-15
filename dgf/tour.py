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


def ts_points_with_beaten_players(position, all_results):
    position_points = TS_POINTS.get(position, 0)
    defeated_players = all_results.count() - position
    return position_points + defeated_players


POINT_SYSTEMS = {
    TS_POINTS_PLUS_BEATEN_PLAYERS: ts_points_with_beaten_players,
}


def get_points(point_system, position, all_results):
    get_points_function = POINT_SYSTEMS.get(point_system)
    if get_points_function is None:
        logger.error(f'Point system \'{point_system}\' does not exist!')
    return get_points_function(position, all_results)
