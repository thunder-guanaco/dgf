from django.test import TestCase

from .utils import create_friends, create_courses
from ...models import Course, Friend, FavoriteCourse
from ...templatetags import dgf


class TemplatetagsFavoriteCoursesTest(TestCase):

    def setUp(self):
        Course.objects.all().delete()
        Friend.objects.all().delete()
        FavoriteCourse.objects.all().delete()

    def test_more_than_one_favorite_course(self):
        mijas, seepark, wischlingen, soehnstetten = create_courses(['DiscGolfPark Mijas',
                                                                    'Seepark Lünen',
                                                                    'Revierpark Wischlingen',
                                                                    'Söhnstetten'])

        create_friends(['user_{}'.format(i) for i in range(6)],
                       favorite_courses=[(),
                                         (mijas,),
                                         (seepark,),
                                         (mijas, wischlingen),
                                         (mijas, wischlingen, seepark),
                                         (mijas, wischlingen, soehnstetten)])

        self.assertListEqual(list(dgf.favorite_courses()), [mijas, wischlingen, seepark])

    def test_favorite_course(self):
        mijas, seepark, wischlingen, soehnstetten = create_courses(['DiscGolfPark Mijas',
                                                                    'Seepark Lünen',
                                                                    'Revierpark Wischlingen',
                                                                    'Söhnstetten'])

        create_friends(['user_{}'.format(i) for i in range(15)],
                       favorite_courses=[(), (), (), (), (),
                                         (mijas,), (mijas,), (mijas,), (mijas,),
                                         (seepark,), (seepark,), (seepark,),
                                         (wischlingen,), (wischlingen,),
                                         (soehnstetten,)])

        self.assertListEqual(list(dgf.favorite_courses()), [mijas, seepark, wischlingen])

    def test_favorite_courses_not_being_favorite(self):
        mijas, seepark, wischlingen, soehnstetten = create_courses(['DiscGolfPark Mijas',
                                                                    'Seepark Lünen',
                                                                    'Revierpark Wischlingen',
                                                                    'Söhnstetten'])

        create_friends(['user_{}'.format(i) for i in range(2)],
                       favorite_courses=[(mijas,), (mijas,)])

        self.assertListEqual(list(dgf.favorite_courses()), [mijas])

    def test_favorite_course_without_favorites(self):
        create_courses(['DiscGolfPark Mijas',
                        'Revierpark Wischlingen',
                        'Söhnstetten'])

        create_friends(['user_{}'.format(i) for i in range(10)])

        self.assertListEqual(list(dgf.favorite_courses()), [])

    def test_favorite_course_without_friends(self):
        create_courses(['DiscGolfPark Mijas',
                        'Revierpark Wischlingen',
                        'Söhnstetten'])

        self.assertListEqual(list(dgf.favorite_courses()), [])

    def test_favorite_course_without_courses(self):
        create_friends(['user_{}'.format(i) for i in range(10)])

        self.assertListEqual(list(dgf.favorite_courses()), [])
