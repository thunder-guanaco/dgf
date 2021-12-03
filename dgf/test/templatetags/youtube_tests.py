from django.test import TestCase

from ...templatetags import dgf


class YoutubeTemplatetagsTest(TestCase):

    def test_youtube_id(self):

        # regular video URL (full URL)
        self.expect_youtube_id(url='https://www.youtube.com/watch?v=3CClOsC26Lw',
                               expected_youtube_id='3CClOsC26Lw')

        # video in playlist
        self.expect_youtube_id(url='https://www.youtube.com/watch?v=ttKn1eGKTew'
                                   '&list=PL_806ww4sa44mmbLuCGXcin35Dv8Yz5ar&index=4',
                               expected_youtube_id='ttKn1eGKTew')

        # shorter share URL
        self.expect_youtube_id(url='https://youtu.be/UhRXn2NRiWI',
                               expected_youtube_id='UhRXn2NRiWI')

        # shorter share URL with timestamp
        self.expect_youtube_id(url='https://youtu.be/FCSBoOcGFFE?t=19',
                               expected_youtube_id='FCSBoOcGFFE')

        # share URL after redirect
        self.expect_youtube_id(url='https://www.youtube.com/watch?v=-pr-xzajQo0&feature=youtu.be',
                               expected_youtube_id='-pr-xzajQo0')

        # broken URL
        self.expect_youtube_id(url='https://www.youtube.comajQo0&feature=youtu.be',
                               expected_youtube_id=None)

        # empty URL
        self.expect_youtube_id(url='',
                               expected_youtube_id=None)

        # no URL
        try:
            self.expect_youtube_id(url=None,
                                   expected_youtube_id=None)
            self.fail('It makes no sense that a URL is None')
        except:
            pass

    def expect_youtube_id(self, url, expected_youtube_id):
        self.assertEqual(dgf.youtube_id(url), expected_youtube_id)
