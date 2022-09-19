import responses

from dgf_cms.settings import GT_LIST_PAGE, GT_ATTENDANCE_PAGE, GT_DETAILS_PAGE, GT_RESULTS_PAGE, GT_RATING_PAGE


def add_list_page(tournament_ids):
    body = ('<body>'
            '  <table class="table table-sm table-striped dataTable no-footer"'
            '      id="list_tournaments" role="grid" aria-describedby="list_tournaments_info">'
            '  <thead></thead>'
            '  <tbody>'
            )

    for tournament_id in tournament_ids:
        body += ('<tr class="odd">'
                 '  <td data-sort="Test Tournament #3" id="table_list_tournaments_0_0">'
                 '    <a class="text-muted font-italic"'
                 f'      href="https://turniere.discgolf.de/index.php?p=events&amp;sp=view&amp;id={tournament_id}">'
                 '        Test Tournament #3'
                 '    </a>'
                 '</tr>'
                 )

    body += ('    </tbody>'
             '  </table>'
             '</body>'
             )

    responses.add(responses.GET, GT_LIST_PAGE, body=body, status=200)


def add_details_page(gt_id, name, dates, canceled=False, pdga_id=None):
    canceled_html = '<b class="text-danger"><i>ABGESAGT</i></b>' if canceled else ''
    if pdga_id:
        pdga_html = f'<a href="https://www.pdga.com/tour/event/{pdga_id}"target="_blank">C-Tier</a>'
    else:
        if pdga_id == 0:
            pdga_html = 'C-Tier'
        else:
            pdga_html = '<span class="glyphicons glyphicons-remove-circle text-danger"></span>'
    responses.add(responses.GET, GT_DETAILS_PAGE.format(gt_id),
                  body='<body>'
                       '  <h2>'
                       f'   {name}'
                       f'   {canceled_html}'
                       '  </h2>'
                       '  <table class="tabletable-sm">'
                       '    <tbody>'
                       '      <tr>'
                       '        <td>Ansprechpartner/Turnierdirektor</td>'
                       '        <td>WHATEVER</td>'
                       '      </tr>'
                       '      <tr>'
                       '        <td>Ort</td>'
                       '        <td><a href="WHAEVER" target="_blank">WHATEVER</a></td>'
                       '      </tr>'
                       '      <tr>'
                       '        <td>Turnierbetrieb</td>'
                       f'       <td>{dates}</td>'
                       '      </tr>'
                       '      <tr>'
                       '        <td>PDGA Status</td>'
                       f'       <td>{pdga_html}</td>'
                       '      </tr>    '
                       '    </tbody>'
                       '  </table>'
                       '</body>',
                  status=200)


def add_attendance_page(tournament_id, player_ids=None, other_format=False):
    body = ('<body>'
            '  <table id="starterlist"'
            '      class="table table-striped table-sm table-hover p-0 m-0 dataTable no-footer"'
            '      style="font-size: 12px; " role="grid" aria-describedby="starterlist_info">'
            '    <thead>'
            '      <tr>'
            '        <th>Division</th>'
            )

    if other_format:
        body += '    <th>Aufr.P</th>'

    body += ('       <th>D-Rating</th>'
             '       <th>Spieler</th>'
             '       <th>Wildcards </th>'
             '       <th>Land</th>'
             '       <th>GT#</th>'
             '       <th>PDGA#</th>'
             '       <th>Angemeldet</th>'
             '       <th>Status</th>'
             '     </tr>'
             '   </thead>'
             '   <tbody>'
             )

    if not player_ids:
        body += ('<tr class="odd">'
                 '  <td valign="top" colspan="9" class="dataTables_empty">'
                 '    Keine Daten in der Tabelle vorhanden'
                 '  </td>'
                 '</tr>'
                 )
    else:
        for player_id in player_ids:
            if player_id:
                body += ('<tr class="p-0 m-0 odd">'
                         '  <td class="p-0 m-0" id="table_starterlist_0_0">WHATEVER</td>'
                         )

                if other_format:
                    body += '<td class="p-0 m-0 sorting_1" id="table_starterlist_0_1">0</td>'

                body += ('  <td class="p-0 m-0" id="table_starterlist_0_1">WHATEVER</td>'
                         '  <td class="p-0 m-0" id="table_starterlist_0_2">WHATEVER</td>'
                         '  <td class="p-0 m-0" data-order="1" id="table_starterlist_0_3">'
                         '    <small><i>(Wildcard)</i></small>'
                         '  </td>'
                         '  <td class="p-0 m-0" id="table_starterlist_0_4">WHATEVER</td>'
                         f' <td class="p-0 m-0" id="table_starterlist_0_5">{player_id}</td>'
                         '  <td class="p-0 m-0" id="table_starterlist_0_6">WHATEVER</td>'
                         '  <td class="p-0 m-0" id="table_starterlist_0_7">WHATEVER</td>'
                         '  <td class="p-0 m-0" id="table_starterlist_0_8">WHATEVER</td>'
                         '</tr>'
                         )
            else:
                body += ('<tr class="p-0 m-0 odd">'
                         '  <td class="p-0 m-0" id="table_starterlist_0_0">'
                         '    <i>Wildcard</i>'
                         '  </td>'
                         '  <td class="p-0 m-0" id="table_starterlist_0_1"></td>'
                         '  <td class="p-0 m-0" id="table_starterlist_0_2"></td>'
                         '  <td class="p-0 m-0" id="table_starterlist_0_3"></td>'
                         '  <td class="p-0 m-0" id="table_starterlist_0_4"></td>'
                         '  <td class="p-0 m-0" id="table_starterlist_0_5"></td>'
                         '  <td class="p-0 m-0" id="table_starterlist_0_6"></td>'
                         '  <td class="p-0 m-0" id="table_starterlist_0_7"></td>'
                         '  <td class="p-0 m-0" id="table_starterlist_0_8"></td>'
                         '</tr>'
                         )

    body += ('    </tbody>'
             '  </table>'
             '</body>'
             )
    responses.add(responses.GET, GT_ATTENDANCE_PAGE.format(tournament_id), body=body, status=200)


def add_empty_results_page(tournament_id):
    responses.add(responses.GET, GT_RESULTS_PAGE.format(tournament_id),
                  body='<body>'
                       '  <div class="mt-1 container alert alert-warning alert-dismissible fade show" role="alert">'
                       '    Es gibt derzeit noch keine endgültigen Ergebnisse.'
                       '    Bitte warten sie bis das Turnier abgeschlossen ist.'
                       '    <button aria-label="Close" class="close" data-dismiss="alert" type="button">'
                       '      <span aria-hidden="true">×</span>'
                       '    </button>'
                       '  </div>'
                       '</body>',
                  status=200)


def add_results_page(tournament_id, results, dnf=None, broken=False):
    body = ('<body>'
            '  <table class="table table-striped table-sm" style="font-size: 12px; " id="results_layout_">'
            '    <thead>'
            '      <tr>'
            )
    if not broken:
        body += '    <th>Division </th>'

    body += ('       <th>#</th>'
             '       <th>Name</th>'
             '       <th>f.Div</th>'
             '       <th>GT#</th>'
             '       <th>par</th>'
             '       <th>R1</th>'
             '       <th>R2</th>'
             '       <th>Gesamt</th>'
             '       <th>Kommentar</th>'
             '     </tr>'
             '   </thead>'
             '   <tbody>'
             )

    for position, gt_id in enumerate(results, start=1):
        body += ('    <tr style="line-height: 10px; min-height: 10px; height: 10px;" class="">'
                 '        <td>O</td>'
                 f'       <td class="text-right" data-order="{position}">{position}</td>'
                 '        <td>Name, Vorname</td>'
                 '        <td></td>'
                 f'       <td>{gt_id}</td>'
                 '        <td>-18</td>'
                 '        <td>49</td>'
                 '        <td>45</td>'
                 '        <td data-order="94">94</td>'
                 '        <td></td>'
                 '      </tr>'
                 )

    if dnf:
        for gt_id in dnf:
            body += ('    <tr style="line-height: 10px; min-height: 10px; height: 10px;" class="">'
                     '        <td>O</td>'
                     f'       <td class="text-right" data-order="9999"> DNF </td>'
                     '        <td>Name, Vorname</td>'
                     '        <td></td>'
                     f'       <td>{gt_id}</td>'
                     '        <td>-</td>'
                     '        <td>49</td>'
                     '        <td>999</td>'
                     '        <td data-order="9999"> DNF </td>'
                     '        <td></td>'
                     '      </tr>'
                     )
    body += ('    </tbody>'
             '  </table>'
             '</body>'
             )

    responses.add(responses.GET, GT_RESULTS_PAGE.format(tournament_id), body=body, status=200)


def add_rating_page(player_id, tournament_ids, include_old_url=False, include_unknown_url=False):
    body = '<body>'
    for gt_id in tournament_ids:
        body += ('  <td style="">'
                 '    <a title="GT Ergebnisse"'
                 '     target="_blank"'
                 f'     href="https://turniere.discgolf.de/index.php?p=events&amp;sp=list-results&amp;id={gt_id}">'
                 '      GT Ergebnisse'
                 '    </a>'
                 '  </td>'
                 )

    if include_old_url:
        body += ('  <td style="">'
                 '    <a title="GT Ergebnisse"'
                 '     target="_blank"'
                 '     href="https://german-tour-online.de/events/results/123">'
                 '      GT Ergebnisse'
                 '    </a>'
                 '  </td>'
                 )

    if include_unknown_url:
        body += ('  <td style="">'
                 '    <a title="GT Ergebnisse"'
                 '     target="_blank"'
                 '     href="http://wft-richard.com/123">'
                 '      GT Ergebnisse'
                 '    </a>'
                 '  </td>'
                 )

    body += '</body>'
    responses.add(responses.GET, GT_RATING_PAGE.format(player_id), body=body, status=200)
