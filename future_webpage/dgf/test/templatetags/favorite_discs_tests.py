from django.test import TestCase

from ...models import Friend, Disc, DiscInBag
from ...templatetags import dgf


class TemplatetagsFavoriteDiscsTest(TestCase):

    def setUp(self):
        Friend.objects.all().delete()
        Disc.objects.all().delete()
        DiscInBag.objects.all().delete()

    def test_favorite_discs(self):
        manolo = Friend.objects.create(username='manolo')
        fede = Friend.objects.create(username='fede')
        mario = Friend.objects.create(username='mario')

        deputy = Disc.objects.create(mold='Deputy')
        aviar = Disc.objects.create(mold='Aviar')

        compass = Disc.objects.create(mold='Compass')
        buzz = Disc.objects.create(mold='Buzzz')

        fd = Disc.objects.create(mold='FD')
        Disc.objects.create(mold='FD2')

        destroyer = Disc.objects.create(mold='Destroyer')

        # a mold is owned only once
        DiscInBag.objects.create(friend=manolo, disc=deputy, amount=1, type=DiscInBag.PUTTER)
        DiscInBag.objects.create(friend=fede, disc=aviar, amount=1, type=DiscInBag.PUTTER)
        DiscInBag.objects.create(friend=mario, disc=aviar, amount=1, type=DiscInBag.PUTTER)

        # someone one mold more than once
        DiscInBag.objects.create(friend=manolo, disc=compass, amount=1, type=DiscInBag.MID_RANGE)
        DiscInBag.objects.create(friend=fede, disc=compass, amount=1, type=DiscInBag.MID_RANGE)
        DiscInBag.objects.create(friend=mario, disc=buzz, amount=5, type=DiscInBag.MID_RANGE)

        # some discs are in no bag
        DiscInBag.objects.create(friend=manolo, disc=fd, amount=2, type=DiscInBag.FAIRWAY_DRIVER)
        DiscInBag.objects.create(friend=fede, disc=fd, amount=1, type=DiscInBag.FAIRWAY_DRIVER)
        DiscInBag.objects.create(friend=mario, disc=fd, amount=1, type=DiscInBag.FAIRWAY_DRIVER)

        # only one disc
        DiscInBag.objects.create(friend=manolo, disc=destroyer, amount=3, type=DiscInBag.DISTANCE_DRIVER)
        DiscInBag.objects.create(friend=fede, disc=destroyer, amount=2, type=DiscInBag.DISTANCE_DRIVER)

        self.assert_favorite_discs(DiscInBag.PUTTER, expect=[aviar, deputy])
        self.assert_favorite_discs(DiscInBag.MID_RANGE, expect=[compass, buzz])
        self.assert_favorite_discs(DiscInBag.FAIRWAY_DRIVER, expect=[fd])
        self.assert_favorite_discs(DiscInBag.DISTANCE_DRIVER, expect=[destroyer])

    def test_favorite_discs_without_bags(self):
        self.assert_favorite_discs(DiscInBag.PUTTER, expect=[])
        self.assert_favorite_discs(DiscInBag.MID_RANGE, expect=[])
        self.assert_favorite_discs(DiscInBag.FAIRWAY_DRIVER, expect=[])
        self.assert_favorite_discs(DiscInBag.DISTANCE_DRIVER, expect=[])

    def assert_favorite_discs(self, type, expect):
        display_names = [disc.display_name for disc in expect]
        self.assertListEqual(list(dgf.favorite_discs(type)), display_names)
