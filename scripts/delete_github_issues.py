import json

import requests

# CONFIG
GITHUB_TOKEN = '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'
FIRST_ISSUE = 4400
LAST_ISSUE = 4433
SEARCH_TERMS = [
    'Manolo: Server error on GET /turniere/tremonia-series/',
]

headers = {'Authorization': f'token {GITHUB_TOKEN}'}
url = 'https://api.github.com/repos/thunder-guanaco/dgf/issues'

print('\nClosing issues matching titles:\n')
for term in SEARCH_TERMS:
    print(f'- {term}')
print('')

closed_amount = 0
for i in range(FIRST_ISSUE, LAST_ISSUE + 1):

    response = requests.get(url + f'/{i}', headers=headers)
    issue = json.loads(response.content)

    if response.status_code >= 400:
        print(f'GitHub API returned {response.status_code}: {response.content}')
        break

    closed = False
    for term in SEARCH_TERMS:
        if term in issue['title']:
            response = requests.patch(url + f'/{i}', json.dumps({"state": "closed"}), headers=headers)
            if response.status_code == 200:
                print(f'Issue #{i} was closed because it matches "{term}"')
                closed_amount += 1
                closed = True
            else:
                print(f'GitHub API returned {response.status_code}: {response.content}')
    if not closed:
        print(f'Issue #{i} was not closed')

print(f'Closed {closed_amount} issues')
