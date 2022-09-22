from pprint import pprint

import requests
from bs4 import BeautifulSoup

RATING_PAGE = 'https://rating.discgolf.de/'
PLAYER_PAGE = 'https://rating.discgolf.de/detail.php?gtn={}'


def find_column(headers, text):
    for i, th in enumerate(headers.find_all('th')):
        if th.text == text:
            return i
    raise IndexError(f'Column with text "{text}" not found!')


def extract_all_gt_numbers():
    rating_page_soup = BeautifulSoup(requests.get(RATING_PAGE).content, features='html5lib')
    table = rating_page_soup.find('table', {'id': 'table'})
    gt_number_column = find_column(table.find('thead'), 'GT-Nummer')

    gt_numbers = []
    for player_tr in table.find('tbody').find_all('tr'):
        gt_number = int(player_tr.find_all('td')[gt_number_column].text)
        gt_numbers.append(gt_number)

    return gt_numbers


def extract_id(url, delimiter):
    return int(url.split(delimiter)[-1])


def extract_id_from_a(a):
    url = a['href']
    if 'turniere.discgolf.de' in url:
        return extract_id(url, '=')
    if 'german-tour-online.de' in url:
        return extract_id(url, '/')
    if 'pdga.com/tour/event' in url:
        return extract_id(url, '/')
    else:
        raise ValueError(f'URL not recognized: {url}')


def get_all_tournament_pairs(gt_number):
    player_page_soup = BeautifulSoup(requests.get(PLAYER_PAGE.format(gt_number)).content, features='html5lib')
    gt_links = player_page_soup.find_all('a', {'title': 'GT Ergebnisse'})

    pairs = set()
    for gt_link in gt_links:
        gt_id = extract_id_from_a(gt_link)

        pdga_link = gt_link.parent.parent.find('a', text='PDGA Ergebnisse')
        pdga_id = extract_id_from_a(pdga_link)

        if pdga_id:
            pairs.add((gt_id, pdga_id))

    return pairs


if __name__ == '__main__':
    gt_numbers = extract_all_gt_numbers()
    gt_pdga_pairs = set()
    for i, gt_number in enumerate(gt_numbers, start=1):
        new_pairs = get_all_tournament_pairs(gt_number)
        gt_pdga_pairs.update(new_pairs)
        if i < 100 or i % 10 == 0:
            print(f'{len(gt_pdga_pairs)} GT/PDGA pairs so far... (already scanned {i} / {len(gt_numbers)} players)')

    pprint(gt_pdga_pairs)
