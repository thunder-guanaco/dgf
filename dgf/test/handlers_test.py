from django.test import TestCase
from dgf.handlers import _filter_sensible_info_out


class HandlersTest(TestCase):

    def filter_sensible_info_out(self):
        filtered_dict = _filter_sensible_info_out({
            'X-Forwarded-For': '95.223.76.243',
            'Host': 'discgolffriends.de',
            'Sec-Fetch-Site': 'same - origin',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': '_ga=123; csrftoken=asd; sessionid=qwe;',
            'csrfmiddlewaretoken': 'qwertyuiop',
            'first_name': 'Manuel',
            'last_name': 'García García',
            'sessid': '1234',
        })
        self.assertTrue('Cookie' not in filtered_dict)
        self.assertTrue('sessid' not in filtered_dict)
        self.assertTrue('123' not in filtered_dict)
        self.assertTrue('asd' not in filtered_dict)
        self.assertTrue('qwe' not in filtered_dict)
        self.assertTrue('csrftoken' not in filtered_dict)
        self.assertTrue('sessionid' not in filtered_dict)
        self.assertTrue('csrfmiddlewaretoken' not in filtered_dict)
        self.assertTrue('qwertyuiop' not in filtered_dict)
