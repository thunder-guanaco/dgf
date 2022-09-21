import logging

from dgf.models import Attendance
from dgf.pdga.common import add_tournament

logger = logging.getLogger(__name__)


def extract_event_ids(events_li):
    events = events_li.find_all('a')
    return [event['href'].split('/')[-1] for event in events]


def get_upcoming_event_ids(player_page_soup):
    upcoming_events = player_page_soup.find('li', {'class': 'upcoming-events'})
    if upcoming_events:
        return extract_event_ids(upcoming_events)

    next_event = player_page_soup.find('li', {'class': 'next-event'})
    if next_event:
        return extract_event_ids(next_event)

    return []


def add_attendance(friend, tournament):
    _, created = Attendance.objects.get_or_create(friend=friend, tournament=tournament)
    if created:
        logger.info(f'Added attendance of {friend} to {tournament}')


def update_tournament_attendance(pdga_api, friend, player_page_soup):
    event_ids = get_upcoming_event_ids(player_page_soup)
    for event_id in event_ids:
        tournament = add_tournament(pdga_api, pdga_id=event_id)
        add_attendance(friend, tournament)
