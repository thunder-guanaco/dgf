from datetime import date, timedelta

import responses

from dgf_cms.settings import PDGA_BASE_URL, PDGA_PAGE_BASE_URL, PDGA_DATE_FORMAT


def add_login():
    responses.add(responses.POST, f'{PDGA_BASE_URL}/user/login',
                  json={'session_name': 'SSESSf1f85588bb869a1781d21eec9fef1bff',
                        'sessid': 'pR2J-dQygl7B8fufkt4YPu-E-KOTeNJsvYyKFLaXXi8',
                        'token': 'uemWB6CbC0qwseuSJ7wogG65FsC7JNBsEXVOnR-xzQc'},
                  status=200)


def add_tournament_data(tournament_id, tournament_name, start_date, end_date):
    search_start_date = date.today()
    search_end_date = date.today() + timedelta(days=400)
    responses.add(responses.GET,
                  f'{PDGA_BASE_URL}/event'
                  f'?tournament_id={tournament_id}'
                  f'&start_date={search_start_date.strftime(PDGA_DATE_FORMAT)}'
                  f'&end_date={search_end_date.strftime(PDGA_DATE_FORMAT)}'
                  f'&offset=0'
                  f'&limit=10',
                  json={'sessid': 'M5EGJLLqYVKIl1b5hczcWrEXfUPYtYWZEz5Fs6JU1oQ',
                        'status': 0,
                        'events': [
                            {
                                'tournament_id': tournament_id,
                                'tournament_name': tournament_name,
                                'city': 'Dortmund',
                                'state_prov': 'NRW',
                                'country': 'Germany',
                                'latitude': '51.519577',
                                'longitude': '7.399750',
                                'start_date': start_date,
                                'end_date': end_date,
                                'class': 'Am',
                                'tier': 'C',
                                'status': 'sanctioned',
                                'format': 'singles',
                                'tournament_director': 'Manuel García García',
                                'tournament_director_pdga_number': '111828',
                                'asst_tournament_director': 'Federico José Sörenson Sánchez',
                                'asst_tournament_director_pdga_number': '109371',
                                'event_email': 'mgg@example.com',
                                'event_phone': '012-345-6789',
                                'event_url': f'https://www.pdga.com/tour/event/{tournament_id}',
                                'website_url': 'https://discgolffriends.de/turniere/tremonia-series',
                                'registration_url': 'https://discgolfmetrix.com/715021',
                                'last_modified': '2021-03-15'
                            }
                        ]},
                  status=200)


def add_player_page_without_events(pdga_number):
    responses.add(responses.GET, f'{PDGA_PAGE_BASE_URL}/player/{pdga_number}', body='<body></body>', status=200)


def add_player_page_with_next_event(pdga_number, tournament_id):
    body = ('<div class="pane-content">'
            '  <ul class="player-info info-list">'
            '    <li class="next-event">'
            '      <strong>Next Event:</strong>'
            f'      <a href="/tour/event/{tournament_id}">WHATEVER</a>'
            '    </li>'
            '  </ul>'
            '</div>'
            )
    responses.add(responses.GET, f'{PDGA_PAGE_BASE_URL}/player/{pdga_number}', body=body, status=200)


def add_player_page_with_upcoming_events(pdga_number, tournament_ids):
    body = ('<div class="pane-content">'
            '  <ul class="player-info info-list">'
            '    <li class="upcoming-events">'
            '      <details open="">'
            '        <summary>'
            '          <strong>Upcoming Events</strong>'
            '        </summary>'
            '        <ul>'
            )

    for tournament_id in tournament_ids:
        body += ('     <li>'
                 f'      <a href="/tour/event/{tournament_id}">WHATEVER</a>'
                 '     </li>'
                 )

    body += ('        </ul>'
             '      </details>'
             '    </li>'
             '  </ul>'
             '</div>'
             )
    responses.add(responses.GET, f'{PDGA_PAGE_BASE_URL}/player/{pdga_number}', body=body, status=200)


def add_year_links(pdga_number, years):
    body = ('<body>'
            '  <div class="pane-content">'
            )

    if not years:
        body += '<p>There is no data available.</p>'

    else:
        body += ('    <div class="year-link">'
                 '      <div class="item-list">'
                 '        <ul class="tabs secondary">'
                 )
        for year in years:
            body += f'      <li><a href="/player/{pdga_number}/stats/{year}">{year}</a></li>'

        body += ('        </ul>'
                 '      </div>'
                 '    </div>'
                 )

    body += ('  </div>'
             '</body>'
             )

    responses.add(responses.GET, f'{PDGA_PAGE_BASE_URL}/player/{pdga_number}', body=body, status=200)


def add_results(pdga_number, year, results):
    body = ('<body>'
            '  <div class="table-container">'
            '    <table>'
            '      <tbody aria-live="polite" aria-relevant="all">'
            )

    for result in results:
        tournament_id, position, division = result
        body += ('    <tr class="WHATEVER">'
                 f'     <td class="place">{position}</td>'
                 '      <td class="points">WHATEVER</td>'
                 '      <td class="tournament">'
                 f'        <a href="/tour/event/{tournament_id}#{division}">WHATEVER</a>'
                 '      </td>'
                 '      <td class="tier">WHATEVER</td>'
                 '      <td class="dates" data-text="WHATEVER">WHATEVER</td>'
                 '    </tr>'
                 )

    body += ('      </tbody>'
             '    </table>'
             '  </div>'
             '</body>'
             )

    responses.add(responses.GET, f'{PDGA_PAGE_BASE_URL}/player/{pdga_number}/stats/{year}', body=body, status=200)
