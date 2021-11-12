from django.test import TestCase

from dgf.handlers import nice_format


class HandlersTest(TestCase):

    def nice_format_test(self):
        formatted_dict = nice_format({
            'X-Forwarded-For': '95.223.76.243',
            'Host': 'discgolffriends.de',
            'Sec-Fetch-Site': 'same - origin',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': '_ga=123; csrftoken=asd; sessionid=qwe;',
            'csrfmiddlewaretoken': 'qwertyuiop',
            'first_name': 'Manuel',
            'last_name': 'García García'
        })
        self.assertTrue('Cookie' not in formatted_dict)
        self.assertTrue('123' not in formatted_dict)
        self.assertTrue('asd' not in formatted_dict)
        self.assertTrue('qwe' not in formatted_dict)
        self.assertTrue('csrftoken' not in formatted_dict)
        self.assertTrue('sessionid' not in formatted_dict)
        self.assertTrue('csrfmiddlewaretoken' not in formatted_dict)
        self.assertTrue('qwertyuiop' not in formatted_dict)
