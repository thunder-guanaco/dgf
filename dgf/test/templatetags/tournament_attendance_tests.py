from datetime import datetime, timedelta

from django.test import TestCase

from ..models.creator import create_friends
from ...models import Friend, Tournament, Attendance
from ...templatetags.dgf import current_tournaments, future_tournaments, now_playing, next_tournaments

TODAY = datetime.today()
YESTERDAY = TODAY - timedelta(days=1)
TOMORROW = TODAY + timedelta(days=1)
THE_DAY_AFTER_TOMORROW = TODAY + timedelta(days=2)


class TemplatetagsTournamentsTest(TestCase):

    def setUp(self):
        Friend.objects.all().delete()
        Tournament.objects.all().delete()
        Attendance.objects.all().delete()
        self.yesterday = Tournament.objects.create(name='yesterday',
                                                   begin=YESTERDAY, end=YESTERDAY)
        self.yesterday_today = Tournament.objects.create(name='yesterday-today',
                                                         begin=YESTERDAY, end=TODAY)
        self.today = Tournament.objects.create(name='today',
                                               begin=TODAY, end=TODAY)
        self.today_2 = Tournament.objects.create(name='today-2',
                                                 begin=TODAY, end=TODAY)
        self.today_tomorrow = Tournament.objects.create(name='today-tomorrow',
                                                        begin=TODAY, end=TOMORROW)
        self.today_the_day_after_tomorrow = Tournament.objects.create(name='today-the-day-after-tomorrow',
                                                                      begin=TODAY, end=THE_DAY_AFTER_TOMORROW)
        self.tomorrow = Tournament.objects.create(name='tomorrow',
                                                  begin=TOMORROW, end=TOMORROW)
        self.tomorrow_2 = Tournament.objects.create(name='tomorrow-2',
                                                    begin=TOMORROW, end=TOMORROW)
        self.tomorrow_the_day_after_tomorrow = Tournament.objects.create(name='tomorrow-the-day-after-tomorrow',
                                                                         begin=TOMORROW,
                                                                         end=THE_DAY_AFTER_TOMORROW)
        self.the_day_after_tomorrow = Tournament.objects.create(name='the-day-after-tomorrow',
                                                                begin=THE_DAY_AFTER_TOMORROW,
                                                                end=THE_DAY_AFTER_TOMORROW)
        self.friends = create_friends(10)

    def test_current_tournaments_without_attendance(self):
        self.assertEqual(current_tournaments().count(), 0)

    def test_current_tournaments_with_attendance(self):
        for i, tournament in enumerate(
                [self.yesterday, self.yesterday_today,
                 self.today, self.today_2, self.today_tomorrow, self.today_the_day_after_tomorrow,
                 self.tomorrow, self.tomorrow_2, self.tomorrow_the_day_after_tomorrow,
                 self.the_day_after_tomorrow]):
            Attendance.objects.create(tournament=tournament, friend=self.friends[i])

        actual = [tournament.name for tournament in current_tournaments()]
        expected = [tournament.name for tournament in [self.yesterday_today,
                                                       self.today, self.today_2, self.today_tomorrow,
                                                       self.today_the_day_after_tomorrow]]
        self.assertEqual(actual, expected)

    def test_current_tournaments_with_some_attendance(self):
        # missing: today_2, today_the_day_after_tomorrow, tomorrow
        for i, tournament in enumerate(
                [self.yesterday, self.yesterday_today,
                 self.today, self.today_tomorrow,
                 self.tomorrow_2, self.tomorrow_the_day_after_tomorrow,
                 self.the_day_after_tomorrow]):
            Attendance.objects.create(tournament=tournament, friend=self.friends[i])

        actual = [tournament.name for tournament in current_tournaments()]
        expected = [tournament.name for tournament in [self.yesterday_today,
                                                       self.today, self.today_tomorrow]]
        self.assertEqual(actual, expected)

    def test_future_tournaments_without_attendance(self):
        self.assertEqual(future_tournaments().count(), 0)

    def test_future_tournaments_with_attendance(self):
        for i, tournament in enumerate(
                [self.yesterday, self.yesterday_today,
                 self.today, self.today_2, self.today_tomorrow, self.today_the_day_after_tomorrow,
                 self.tomorrow, self.tomorrow_2, self.tomorrow_the_day_after_tomorrow,
                 self.the_day_after_tomorrow]):
            Attendance.objects.create(tournament=tournament, friend=self.friends[i])

        actual = [tournament.name for tournament in future_tournaments()]
        expected = [tournament.name for tournament in
                    [self.tomorrow, self.tomorrow_2, self.tomorrow_the_day_after_tomorrow,
                     self.the_day_after_tomorrow]]
        self.assertEqual(actual, expected)

    def test_future_tournaments_with_some_attendance(self):
        # missing: today_2, today_the_day_after_tomorrow, tomorrow
        for i, tournament in enumerate(
                [self.yesterday, self.yesterday_today,
                 self.today, self.today_tomorrow,
                 self.tomorrow_2, self.tomorrow_the_day_after_tomorrow,
                 self.the_day_after_tomorrow]):
            Attendance.objects.create(tournament=tournament, friend=self.friends[i])

        actual = [tournament.name for tournament in future_tournaments()]
        expected = [tournament.name for tournament in [self.tomorrow_2, self.tomorrow_the_day_after_tomorrow,
                                                       self.the_day_after_tomorrow]]
        self.assertEqual(actual, expected)

    def test_now_playing(self):
        for i, tournament in enumerate(
                [self.yesterday, self.yesterday_today,
                 self.today, self.today_2, self.today_tomorrow, self.today_the_day_after_tomorrow,
                 self.tomorrow, self.tomorrow_2, self.tomorrow_the_day_after_tomorrow,
                 self.the_day_after_tomorrow]):
            Attendance.objects.create(tournament=tournament, friend=self.friends[i])

        self.expect(now_playing(self.friends[0]), [])  # yesterday
        self.expect(now_playing(self.friends[1]), [self.yesterday_today])
        self.expect(now_playing(self.friends[2]), [self.today])
        self.expect(now_playing(self.friends[3]), [self.today_2])
        self.expect(now_playing(self.friends[4]), [self.today_tomorrow])
        self.expect(now_playing(self.friends[5]), [self.today_the_day_after_tomorrow])
        self.expect(now_playing(self.friends[6]), [])  # tomorrow
        self.expect(now_playing(self.friends[7]), [])  # tomorrow_2
        self.expect(now_playing(self.friends[8]), [])  # tomorrow_the_day_after_tomorrow
        self.expect(now_playing(self.friends[9]), [])  # the_day_after_tomorrow

    def test_next_tournaments(self):
        for i, tournament in enumerate(
                [self.yesterday, self.yesterday_today,
                 self.today, self.today_2, self.today_tomorrow, self.today_the_day_after_tomorrow,
                 self.tomorrow, self.tomorrow_2, self.tomorrow_the_day_after_tomorrow,
                 self.the_day_after_tomorrow]):
            Attendance.objects.create(tournament=tournament, friend=self.friends[i])

        self.expect(next_tournaments(self.friends[0]), [])  # yesterday
        self.expect(next_tournaments(self.friends[1]), [])  # yesterday_today
        self.expect(next_tournaments(self.friends[2]), [])  # self.today
        self.expect(next_tournaments(self.friends[3]), [])  # self.today_2
        self.expect(next_tournaments(self.friends[4]), [])  # self.today_tomorrow
        self.expect(next_tournaments(self.friends[5]), [])  # self.today_the_day_after_tomorrow
        self.expect(next_tournaments(self.friends[6]), [self.tomorrow])
        self.expect(next_tournaments(self.friends[7]), [self.tomorrow_2])
        self.expect(next_tournaments(self.friends[8]), [self.tomorrow_the_day_after_tomorrow])
        self.expect(next_tournaments(self.friends[9]), [self.the_day_after_tomorrow])

    def expect(self, actual, expected):
        self.assertEqual([tournament.name for tournament in actual],
                         [tournament.name for tournament in expected])
