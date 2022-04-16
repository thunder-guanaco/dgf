import requests
import json

# CONFIG
GITHUB_TOKEN = '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'
RANGE = range(2600, 2900)
SEARCH_TERMS = ['Manolo: Server error on POST /cookies/decline/analytics/',
                'Anonymous user: Server error on POST /cookies/decline/analytics,google,facebook',
                'Anonymous user: Server error on POST /cookies/decline/analytics/']

headers = {'Authorization': f'token {GITHUB_TOKEN}'}
url = 'https://api.github.com/repos/thunder-guanaco/dgf/issues'

for i in RANGE:

    response = requests.get(url + f'/{i}', headers=headers)
    issue = json.loads(response.content)

    if response.status_code >= 400:
        print(f'GitHub API returned {response.status_code}: {response.content}')
        break

    for term in SEARCH_TERMS:
        if term in issue['title']:
            print(f'closing issue with number: {i}')
            response = requests.patch(url + f'/{i}', json.dumps({"state": "closed"}), headers=headers)
            if response.status_code == 200:
                print(f'closed issue with number: {i}')
            else:
                print(f'GitHub API returned {response.status_code}: {response.content}')
        else:
            print(f'did not close issue with number {i}')
