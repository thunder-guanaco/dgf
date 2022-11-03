import logging

from dgf.german_tour.common import get, find_column
from dgf.models import Friend, Result, Division
from dgf_cms.settings import GT_RESULTS_PAGE

logger = logging.getLogger(__name__)


def parse_gt_number(gt_number_text):
    return int(gt_number_text) if gt_number_text.strip() else None


DIVISION_MAPPING = {
    'O': 'MPO',
    'W': 'FPO',
    'M40': 'MP40',
    'M50': 'MP50',
    'M55': 'MP55',
    'M60': 'MP60',
    'M70': 'MP70',
    'WM40': 'FP40',
}


def parse_division(division_id):
    if not division_id:
        return None

    division_id = DIVISION_MAPPING.get(division_id, division_id)
    try:
        return Division.objects.get(id=division_id)
    except Division.DoesNotExist as e:
        # We do not want to create divisions that do not exist automatically...
        # The German Tour has weird divisions that normally have a matching PDGA division (but it's called different)
        # Therefore this should fail and the found division will be either added to the mapping above or added manually
        e.args = (*e.args, f'division id="{division_id}"')
        raise e


def parse_position(position_text):
    if 'DNF' in position_text:
        return None

    if not position_text:
        return None

    return int(position_text)


def create_result(friend, tournament, position, division):
    result, created = Result.objects.get_or_create(tournament=tournament,
                                                   friend=friend,
                                                   defaults={'position': position})

    result.division = division  # update division (some results might not have one)
    result.save()

    if created:
        logger.info(f'Added result: {result}')


def update_results_from_table(results_header, results_content, tournament):
    gt_number_i = find_column(results_header, 'GT#')
    division_i = find_column(results_header, 'Division ')
    position_i = find_column(results_header, '#')
    for tr in results_content.find_all('tr'):

        gt_number = parse_gt_number(tr.find_all('td')[gt_number_i].text)
        if not gt_number:
            continue  # not someone we are interested in, all Friends have a GT number

        division = parse_division(tr.find_all('td')[division_i].text.strip())
        position = parse_position(tr.find_all('td')[position_i].text.strip())
        if not position:
            continue  # no position, maybe DNF?

        try:
            friend = Friend.objects.get(gt_number=gt_number)
            create_result(friend, tournament, position, division)
        except Friend.DoesNotExist:
            pass  # it's not a Friend, ignore them


def tournament_has_no_results(results_soup):
    alert_warning = results_soup.find('div', {'class': 'alert-warning'})
    return alert_warning and 'Bitte warten sie bis das Turnier abgeschlossen ist.' in alert_warning.text


def update_tournament_results(tournament):
    results_soup = get(GT_RESULTS_PAGE.format(tournament.gt_id))

    if tournament_has_no_results(results_soup):
        logger.info(f'Tournament {tournament} (PDGA={tournament.pdga_id}, GT={tournament.gt_id}) has no results yet')
        return

    results_tables = results_soup.find_all('table')
    for results_table in results_tables:
        table_header = results_table.find('thead')
        table_content = results_table.find('tbody')
        update_results_from_table(table_header, table_content, tournament)
