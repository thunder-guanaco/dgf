import json

import requests

from delete_github_issues_config import GITHUB_TOKEN, SEARCH_TERMS, FIRST_ISSUE, LAST_ISSUE

headers = {'Authorization': f'token {GITHUB_TOKEN}'}
url = 'https://api.github.com/repos/thunder-guanaco/dgf/issues'

print(f'\nScanning issues from {FIRST_ISSUE} to {LAST_ISSUE}.')
print('Looking for the ones matching titles:\n')
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
        if term in issue['title'] or (issue['body'] and term in issue['body']):
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
