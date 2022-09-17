import logging

from dgf.german_tour.common import get, add_tournament, find_column, extract_gt_id, parse_tournament_from_details_page
from dgf.models import Friend, Result, Division
from dgf_cms.settings import GT_RATINGS_PAGE, GT_DETAILS_PAGE, GT_RESULTS_PAGE

logger = logging.getLogger(__name__)


def get_all_tournaments_from_ratings_page():
    tournament_ids = set()
    for friend in Friend.objects.filter(gt_number__isnull=False):
        player_page_soup = get(GT_RATINGS_PAGE.format(friend.gt_number))
        result_links = player_page_soup.findAll('a', title='GT Ergebnisse')
        for link in result_links:

            url = link['href']
            if 'turniere.discgolf.de' in url:
                tournament_id = extract_gt_id(url)
                tournament_ids.add(tournament_id)
            elif 'german-tour-online.de' in url:
                # we do not parse these URLS anymore since https://german-tour-online.de is not live anymore
                pass
            else:
                raise ValueError(f'Tournament URL not recognized: {url}')

    return tournament_ids


def parse_gt_number(gt_number_text):
    return int(gt_number_text) if gt_number_text.strip() else None


DIVISION_MAPPING = {
    'O': 'MPO',
    'W': 'FPO',
    'M40': 'MP40',
    'M50': 'MP50',
    'M60': 'MP60',
    'M70': 'MP70',
    'WM40': 'FP40',
}


def parse_division(division_text):
    division_id = DIVISION_MAPPING.get(division_text, division_text)
    try:
        return Division.objects.get(id=division_id)
    except Division.DoesNotExist as e:
        logger.error(f'Division "{division_text}" does not exist')
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


def update_tournament_results(tournament):
    results_soup = get(GT_RESULTS_PAGE.format(tournament.gt_id))

    results_tables = results_soup.find_all('table')
    for results_table in results_tables:
        table_header = results_table.find('thead')
        table_content = results_table.find('tbody')
        update_results_from_table(table_header, table_content, tournament)


def update_all_tournaments_results():
    tournament_ids = get_all_tournaments_from_ratings_page()
    logger.info(f'{len(tournament_ids)} tournaments to import')
    for tournament_id in tournament_ids:
        logger.info('\n-------------------------------------------')
        gt_tournament = parse_tournament_from_details_page(tournament_id)
        tournament = add_tournament(gt_tournament)
        update_tournament_results(tournament)
