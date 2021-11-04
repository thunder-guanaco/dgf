from datetime import date, timedelta

from cms.api import add_plugin
from cms.models import Placeholder
from django.test import TestCase
from parameterized import parameterized

from ...cms_plugins import FriendPluginPublisher, FriendsHeaderPluginPublisher, SmallerFriendPluginPublisher, \
    BiggerFriendPluginPublisher, UdiscPluginPublisher, GoogleCalendarPluginPublisher, \
    TremoniaSeriesNextTournamentsPluginPublisher, TremoniaSeriesHallOfFamePluginPublisher, \
    TremoniaSeriesHallOfFamePagePluginPublisher
from ...models import Friend, Course, UdiscRound, Tournament, Result

PAST_DAY = date(year=2000, month=1, day=1)
FUTURE_DAY = date(year=3000, month=1, day=1)


class DgfPluginsTests(TestCase):

    @parameterized.expand([
        (FriendPluginPublisher,),
        (SmallerFriendPluginPublisher,),
        (BiggerFriendPluginPublisher,),
    ])
    def test_friend_plugin(self, plugin_class):
        friend = self.create_1_user('test')

        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            plugin_class,
            'en',
            target=None,
            friend=friend
        )
        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render({}, model_instance, None)

        self.assertEqual(context['friend'].username, 'test')

    def test_friends_header_plugin(self):
        self.create_3_friends()

        context = self.render_plugin(FriendsHeaderPluginPublisher)

        self.assertEqual({friend.username for friend in context['friends']},
                         {'test_0', 'test_1', 'test_2'})

    def test_udisc_plugin(self):
        friends = self.create_3_friends()
        course = self.create_1_course('test', '1234')
        self.create_3_rounds(course, friends, [60, 55, 70])

        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            UdiscPluginPublisher,
            'en',
            target=None,
            course=course
        )
        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render({}, model_instance, None)

        self.assertEqual(context['course_url'], 'https://udisc.com/courses/1234')
        self.assertEqual([(round.friend.username, round.score) for round in context['rounds']],
                         [('test_1', 55), ('test_0', 60), ('test_2', 70)])
        self.assertEqual(context['course'], course)

    def test_google_calendar_plugin(self):
        self.render_plugin(GoogleCalendarPluginPublisher)

    @parameterized.expand([
        (TremoniaSeriesHallOfFamePluginPublisher,),
        (TremoniaSeriesHallOfFamePagePluginPublisher,),
    ])
    def test_tremonia_series_hall_of_fame_plugin(self, plugin_class):
        friends = self.create_3_friends()
        tournaments = self.create_tournaments()
        Result.objects.all().delete()

        Result.objects.create(friend=friends[0], tournament=tournaments[1], position=1)
        Result.objects.create(friend=friends[0], tournament=tournaments[3], position=3)
        Result.objects.create(friend=friends[0], tournament=tournaments[4], position=1)

        Result.objects.create(friend=friends[1], tournament=tournaments[1], position=1)
        Result.objects.create(friend=friends[1], tournament=tournaments[3], position=1)
        Result.objects.create(friend=friends[1], tournament=tournaments[4], position=2)

        Result.objects.create(friend=friends[2], tournament=tournaments[0], position=1)  # not TS
        Result.objects.create(friend=friends[2], tournament=tournaments[1], position=3)
        Result.objects.create(friend=friends[2], tournament=tournaments[2], position=1)  # not TS
        Result.objects.create(friend=friends[2], tournament=tournaments[3], position=2)
        Result.objects.create(friend=friends[2], tournament=tournaments[4], position=1)

        context = self.render_plugin(plugin_class)

        self.assertEqual([friend.username for friend in context['friends']], ['test_1', 'test_0', 'test_2'])

    def test_tremonia_series_next_tournaments_plugin(self):
        self.create_tournaments()

        context = self.render_plugin(TremoniaSeriesNextTournamentsPluginPublisher)

        self.assertEqual([tournament.name for tournament in context['tournaments']],
                         ['Tremonia Series #8888', 'Tremonia Series #9999'])

    def render_plugin(self, plugin_class):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            plugin_class,
            'en',
            target=None,
        )
        plugin_instance = model_instance.get_plugin_class_instance()
        return plugin_instance.render({}, model_instance, None)

    def create_1_user(self, username):
        Friend.objects.all().delete()
        return Friend.objects.create(username=username, first_name=username)

    def create_3_friends(self):
        Friend.objects.all().delete()
        return [Friend.objects.create(username=f'test_{i}',
                                      first_name=f'test_{i}') for i
                in range(3)]

    def create_1_course(self, name, udisc_id):
        Course.objects.all().delete()
        return Course.objects.create(name=name,
                                     udisc_id=udisc_id)

    def create_3_rounds(self, course, friends, scores):
        UdiscRound.objects.all().delete()
        return [UdiscRound.objects.create(course=course,
                                          friend=friend,
                                          score=scores[i])
                for i, friend in enumerate(friends)]

    def create_tournaments(self):
        Tournament.objects.all().delete()
        return [
            Tournament.objects.create(begin=PAST_DAY,
                                      end=PAST_DAY,
                                      name='Tremonia Open 2000',
                                      url='http://example.com/to2000'),

            Tournament.objects.create(begin=PAST_DAY,
                                      end=PAST_DAY,
                                      name='Tremonia Series #1',
                                      url='http://example.com/ts1'),

            Tournament.objects.create(begin=FUTURE_DAY,
                                      end=FUTURE_DAY,
                                      name='Tremonia Open 3000',
                                      url='http://example.com/to3000'),

            Tournament.objects.create(begin=FUTURE_DAY + timedelta(days=1),
                                      end=FUTURE_DAY + timedelta(days=1),
                                      name='Tremonia Series #9999',
                                      url='http://example.com/ts9999'),

            Tournament.objects.create(begin=FUTURE_DAY,
                                      end=FUTURE_DAY,
                                      name='Tremonia Series #8888',
                                      url='http://example.com/ts8888'),
        ]
