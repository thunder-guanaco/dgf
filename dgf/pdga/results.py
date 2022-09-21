import logging

from dgf.models import Division, Result
from dgf.pdga.common import get_page, add_tournament

logger = logging.getLogger(__name__)


def get_year_links(player_page_soup):
    year_links = player_page_soup.find('div', {'class': 'year-link'})
    if year_links:
        return [li.find('a').attrs['href'] for li in year_links.find_all('li')]
    else:
        return []


def add_result(friend, tournament, position, division):
    # get_or_create because we want to create legacy divisions
    division, created = Division.objects.get_or_create(id=division)
    if created:
        logger.info(f'Created division {division}')

    result, created = Result.objects.get_or_create(tournament=tournament,
                                                   friend=friend,
                                                   defaults={
                                                       'position': position,
                                                       'division': division
                                                   })
    if created:
        logger.info(f'Added result: {result}')


def add_tournament_results(pdga_api, friend, year_link):
    year_page_soup = get_page(year_link)
    tables = year_page_soup.find_all('div', {'class': 'table-container'})
    for table in tables:
        trs = table.find('tbody').find_all('tr')
        for tr in trs:
            division = tr.find('td', {'class': 'tournament'}).find('a')['href'].split('#')[1]
            position = int(tr.find('td', {'class': 'place'}).text)
            tournament_url = tr.find('td', {'class': 'tournament'}).find('a').attrs['href']
            tournament_id = tournament_url.split('#')[0].split('/')[-1]
            tournament = add_tournament(pdga_api, pdga_id=tournament_id)
            add_result(friend, tournament, position, division)


def update_tournament_results(pdga_api, friend, player_page_soup):
    year_links = get_year_links(player_page_soup)
    for link in year_links:
        add_tournament_results(pdga_api, friend, link)
