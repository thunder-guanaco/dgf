from datetime import datetime

from django.test import TestCase

from ..models import Course, Friend, Disc, DiscInBag, Ace
from ..templatetags import dgf


class TemplatetagsTest(TestCase):

    def setUp(self):
        Course.objects.all().delete()
        Friend.objects.all().delete()
        Disc.objects.all().delete()
        DiscInBag.objects.all().delete()

    def test_favorite_course(self):
        mijas, wischlingen, soehnstetten = self.create_courses(['DiscGolfPark Mijas',
                                                                'Revierpark Wischlingen',
                                                                'Söhnstetten'])

        self.create_friends(['user_{}'.format(i) for i in range(10)], favorite_courses=[mijas, mijas, mijas,
                                                                                        wischlingen, wischlingen,
                                                                                        soehnstetten,
                                                                                        None, None, None, None])
        self.assertEquals(dgf.favorite_course(), mijas.name)

    def test_favorite_course_without_favorites(self):
        self.create_courses(['DiscGolfPark Mijas',
                             'Revierpark Wischlingen',
                             'Söhnstetten'])

        self.create_friends(['user_{}'.format(i) for i in range(10)])

        self.assertEquals(dgf.favorite_course(), '')

    def test_favorite_course_without_friends(self):
        self.create_courses(['DiscGolfPark Mijas',
                             'Revierpark Wischlingen',
                             'Söhnstetten'])

        self.assertEquals(dgf.favorite_course(), '')

    def test_favorite_course_without_courses(self):
        self.create_friends(['user_{}'.format(i) for i in range(10)])

        self.assertEquals(dgf.favorite_course(), '')

    def test_all_aces(self):
        manolo = Friend.objects.create(username='manolo')
        fd = Disc.objects.create(mold='FD')
        wischlingen = Course.objects.create(name='Wischlingen')
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5')
        self.assertEquals(dgf.all_aces().count(), 1)

    def test_all_aces_without_aces(self):
        self.assertEquals(dgf.all_aces().count(), 0)

    def test_aces_for_user(self):

        manolo = Friend.objects.create(username='manolo')
        fd = Disc.objects.create(mold='FD')
        wischlingen = Course.objects.create(name='Wischlingen')

        # before current year
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=datetime(year=datetime.now().year - 2, month=1, day=1))
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=datetime(year=datetime.now().year - 2, month=1, day=1))
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.CASUAL_ROUND,
                           date=datetime(year=datetime.now().year - 2, month=1, day=1))
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=datetime(year=datetime.now().year - 1, month=1, day=1))

        # current year
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=datetime(year=datetime.now().year, month=1, day=1))
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.PRACTICE,
                           date=datetime(year=datetime.now().year, month=1, day=1))

        self.assertEquals(dgf.before_current_year(manolo.aces), 4)
        self.assertEquals(dgf.before_current_year_tournaments(manolo.aces), 3)
        self.assertEquals(dgf.current_year(manolo.aces), 2)
        self.assertEquals(dgf.current_year_tournaments(manolo.aces), 1)

    def test_aces_for_all_users(self):
        manolo = Friend.objects.create(username='manolo')
        fede = Friend.objects.create(username='fede')
        fd = Disc.objects.create(mold='FD')
        wischlingen = Course.objects.create(name='Wischlingen')

        # before current year
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=datetime(year=datetime.now().year - 2, month=1, day=1))
        Ace.objects.create(friend=fede, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=datetime(year=datetime.now().year - 2, month=1, day=1))
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.CASUAL_ROUND,
                           date=datetime(year=datetime.now().year - 2, month=1, day=1))
        Ace.objects.create(friend=fede, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=datetime(year=datetime.now().year - 1, month=1, day=1))

        # current year
        Ace.objects.create(friend=manolo, disc=fd, course=wischlingen, hole='5', type=Ace.TOURNAMENT,
                           date=datetime(year=datetime.now().year, month=1, day=1))
        Ace.objects.create(friend=fede, disc=fd, course=wischlingen, hole='5', type=Ace.PRACTICE,
                           date=datetime(year=datetime.now().year, month=1, day=1))

        all_aces = Ace.objects.all()
        self.assertEquals(dgf.before_current_year(all_aces), 4)
        self.assertEquals(dgf.before_current_year_tournaments(all_aces), 3)
        self.assertEquals(dgf.current_year(all_aces), 2)
        self.assertEquals(dgf.current_year_tournaments(all_aces), 1)

    def test_aces_no_aces(self):
        Friend.objects.create(username='manolo')
        Friend.objects.create(username='fede')
        Disc.objects.create(mold='FD')
        Course.objects.create(name='Wischlingen')

        all_aces = Ace.objects.all()
        self.assertEquals(dgf.before_current_year(all_aces), 0)
        self.assertEquals(dgf.before_current_year_tournaments(all_aces), 0)
        self.assertEquals(dgf.current_year(all_aces), 0)
        self.assertEquals(dgf.current_year_tournaments(all_aces), 0)

    def test_aces_no_users(self):
        all_aces = Ace.objects.all()
        self.assertEquals(dgf.before_current_year(all_aces), 0)
        self.assertEquals(dgf.before_current_year_tournaments(all_aces), 0)
        self.assertEquals(dgf.current_year(all_aces), 0)
        self.assertEquals(dgf.current_year_tournaments(all_aces), 0)

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

        self.assertListEqual(list(dgf.favorite_discs(DiscInBag.PUTTER)), self.display_names(aviar, deputy))
        self.assertListEqual(list(dgf.favorite_discs(DiscInBag.MID_RANGE)), self.display_names(compass, buzz))
        self.assertListEqual(list(dgf.favorite_discs(DiscInBag.FAIRWAY_DRIVER)), self.display_names(fd))
        self.assertListEqual(list(dgf.favorite_discs(DiscInBag.DISTANCE_DRIVER)), self.display_names(destroyer))

    def test_favorite_discs_without_bags(self):
        self.assertListEqual(list(dgf.favorite_discs(DiscInBag.PUTTER)), [])
        self.assertListEqual(list(dgf.favorite_discs(DiscInBag.MID_RANGE)), [])
        self.assertListEqual(list(dgf.favorite_discs(DiscInBag.FAIRWAY_DRIVER)), [])
        self.assertListEqual(list(dgf.favorite_discs(DiscInBag.DISTANCE_DRIVER)), [])

    def display_names(self, *args):
        return [disc.display_name for disc in args]

    def create_courses(self, course_names):

        new_courses = []

        for name in course_names:
            new_course = Course.objects.create(name=name)
            new_courses.append(new_course)

        return new_courses

    def create_friends(self, usernames, favorite_courses=None):

        new_friends = []

        if type(favorite_courses) != list:
            favorite_courses = [favorite_courses for _ in range(len(usernames))]

        for i, username in enumerate(usernames):
            new_friend = Friend.objects.create(username=username, favorite_course=favorite_courses[i])
            new_friends.append(new_friend)

        return new_friends
