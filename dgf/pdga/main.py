import logging

from dgf.pdga.attendance import update_tournament_attendance
from dgf.pdga.common import get_player_page
from dgf.pdga.results import update_tournament_results

logger = logging.getLogger(__name__)


def update_friend_tournaments(friend, pdga_api):
    if friend.pdga_number:
        player_page_soup = get_player_page(friend.pdga_number)
        update_tournament_attendance(pdga_api, friend, player_page_soup)
        update_tournament_results(pdga_api, friend, player_page_soup)
