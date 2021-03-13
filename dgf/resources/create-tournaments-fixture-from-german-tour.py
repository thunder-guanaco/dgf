import csv
import json

model = "dgf.tournament"


def getDate(date_string, index):
    if '-' in date_string:
        # composed date...
        splitted = date_string.split('-')
        year = splitted[1].split('.')[2]
        german_date = splitted[index].strip().split('.')
        day = german_date[0]
        month = german_date[1]
    else:
        german_date = date_string.split('.')
        day = german_date[0]
        month = german_date[1]
        year = german_date[2]
    return f'20{year}-{month}-{day}'


with open('tournaments.csv', 'r') as csv_file:
    tournament_reader = csv.DictReader(csv_file, delimiter=';', quotechar='"')
    tournaments = list()
    for row in tournament_reader:
        tournament = {'model': model, 'fields': dict()}
        tournament['fields']['name'] = row['Tournament']
        tournament['fields']['begin'] = getDate(row['Date'], 0)
        tournament['fields']['end'] = getDate(row['Date'], 1)
        if 'ABGESAGT' not in tournament['fields']['name']:
            tournaments.append(tournament)

    new_fixture = open('tournaments.json', 'w')
    new_fixture.write(json.dumps(tournaments, indent=2))
    new_fixture.close()
