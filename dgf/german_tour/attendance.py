import logging

from dgf.german_tour.common import get, find_column
from dgf.models import Friend, Attendance
from dgf_cms.settings import GT_ATTENDANCE_PAGE

logger = logging.getLogger(__name__)


def extract_gt_numbers(attendance_header, attendance_content):
    gt_numbers = []
    gt_number_i = find_column(attendance_header, 'GT#')
    for tr in attendance_content.find_all('tr'):
        text = tr.find_all('td')[gt_number_i].text
        if text:
            gt_numbers.append(int(text))
    return gt_numbers


def update_tournament_attendance(tournament):
    attendance_soup = get(GT_ATTENDANCE_PAGE.format(tournament.gt_id))
    attendance_table = attendance_soup.find('table', id='starterlist')
    table_header = attendance_table.find('thead')
    table_content = attendance_table.find('tbody')

    if 'Keine Daten in der Tabelle vorhanden' in [td.text.strip() for td in table_content.find_all('td')]:
        logger.info(f'No attendance list for tournament {tournament}')
        return

    gt_numbers = extract_gt_numbers(table_header, table_content)
    for friend in Friend.objects.filter(gt_number__in=gt_numbers):
        _, created = Attendance.objects.get_or_create(friend=friend, tournament=tournament)
        if created:
            logger.info(f'Added attendance of {friend} to {tournament}')
