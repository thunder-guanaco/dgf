import requests

EMAIL = 'marianocucufate@gmail.com'
PASSWORD = ''

COMPETITION_ID = 749196
LANG = 'es'
DESCRIPTION = '<p>holaquease</p>'

login_get_response = requests.get('https://discgolfmetrix.com/?u=login')
php_session_id = login_get_response.cookies.get('PHPSESSID')

requests.post('https://discgolfmetrix.com/?u=login',
              headers={'Cookie': f'PHPSESSID={php_session_id}'},
              data=[
                  ('email', EMAIL),
                  ('password', PASSWORD),
                  ('Login', 'Entrar')
              ])

requests.post(f'https://discgolfmetrix.com/?u=competition_description&lang=es&ID={COMPETITION_ID}',
              headers={'Cookie': f'PHPSESSID={php_session_id}'},
              data=[
                  ('lang', LANG),
                  ('description', DESCRIPTION),
                  ('Action', 'Guardar')
              ])
