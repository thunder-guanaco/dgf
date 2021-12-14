from datetime import datetime, timedelta, date

from django.test import TestCase

from ..models.creator import create_friends, create_tournaments
from ...models import Friend, Tournament, Attendance, Result
from ...templatetags.dgf import current_tournaments, future_tournaments, now_playing, next_tournaments, \
    problematic_tournaments, active_attendance, attends, podium_results

TODAY = datetime.today()
YESTERDAY = TODAY - timedelta(days=1)
TOMORROW = TODAY + timedelta(days=1)
THE_DAY_AFTER_TOMORROW = TODAY + timedelta(days=2)


class TournamentsTemplatetagsTest(TestCase):

    def setUp(self):
        Friend.objects.all().delete()
        Tournament.objects.all().delete()
        Attendance.objects.all().delete()
        Result.objects.all().delete()
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

    def test_attends(self):
        tournament = create_tournaments(1)
        friends = create_friends(3)
        tournament.attendance.create(friend=friends[0])
        tournament.attendance.create(friend=friends[1])
        self.assertTrue(attends(tournament, friends[0]))
        self.assertTrue(attends(tournament, friends[1]))
        self.assertFalse(attends(tournament, friends[2]))

    def test_active_attendance(self):
        tournament = create_tournaments(1)
        friends = create_friends(3)
        friends[2].is_active = False
        friends[2].save()
        tournament.attendance.create(friend=friends[0])
        tournament.attendance.create(friend=friends[1])
        tournament.attendance.create(friend=friends[2])

        filtered_friends = {attendance.friend.username for attendance in active_attendance(tournament)}
        expected_friends = {friend.username for friend in friends[0:2]}

        self.assertEqual(filtered_friends, expected_friends)

    def test_problematic_tournaments(self):
        tournaments = create_tournaments(24)
        for tournament in tournaments[:12]:
            tournament.name = f'Tremonia Series {tournament.name}'
            tournament.save()
        friends = create_friends(4)

        # ok
        self.create_results(tournaments[0], friends, in_positions=[])  # empty results
        self.create_results(tournaments[1], friends, in_positions=[1, 2, 3, 4])

        # problematic
        self.create_results(tournaments[2], friends, in_positions=[1, 2, 3, 3])
        self.create_results(tournaments[3], friends, in_positions=[1, 2, 2, 3])
        self.create_results(tournaments[4], friends, in_positions=[1, 2, 2, 4])
        self.create_results(tournaments[5], friends, in_positions=[1, 2, 2, 2])
        self.create_results(tournaments[6], friends, in_positions=[1, 1, 3, 4])
        self.create_results(tournaments[7], friends, in_positions=[1, 1, 3, 3])
        self.create_results(tournaments[8], friends, in_positions=[1, 1, 1, 2])
        self.create_results(tournaments[9], friends, in_positions=[1, 1, 1, 3])
        self.create_results(tournaments[10], friends, in_positions=[1, 1, 1, 4])
        self.create_results(tournaments[11], friends, in_positions=[1, 1, 1, 1])

        # problematic but not TS
        self.create_results(tournaments[12], friends, in_positions=[1, 2, 3, 3])
        self.create_results(tournaments[13], friends, in_positions=[1, 2, 2, 3])
        self.create_results(tournaments[14], friends, in_positions=[1, 2, 2, 4])
        self.create_results(tournaments[15], friends, in_positions=[1, 2, 2, 2])
        self.create_results(tournaments[16], friends, in_positions=[1, 1, 3, 4])
        self.create_results(tournaments[17], friends, in_positions=[1, 1, 3, 3])
        self.create_results(tournaments[18], friends, in_positions=[1, 1, 1, 2])
        self.create_results(tournaments[19], friends, in_positions=[1, 1, 1, 3])
        self.create_results(tournaments[20], friends, in_positions=[1, 1, 1, 4])
        self.create_results(tournaments[21], friends, in_positions=[1, 1, 1, 1])

        # ok and not TS
        self.create_results(tournaments[22], friends, in_positions=[])  # empty results
        self.create_results(tournaments[23], friends, in_positions=[1, 2, 3, 4])

        problematic_tournament_names = [tournament.name for tournament in problematic_tournaments()]
        expected_problematic_tournament_names = [tournament.name for tournament in tournaments[2:12]]

        self.assertEqual(problematic_tournament_names, expected_problematic_tournament_names)

    def create_results(self, tournament, friends, in_positions):
        for i, position in enumerate(in_positions):
            Result.objects.create(tournament=tournament, friend=friends[i], position=position)

    def test_podium_results_without_results(self):
        friend = create_friends(1)
        create_tournaments(10)
        self.assert_podiums(friend, [])

    def test_podium_results(self):
        friend = create_friends(1)
        tournaments = self.create_tournaments(10)
        Result.objects.create(friend=friend, tournament=tournaments[0], position=1)
        Result.objects.create(friend=friend, tournament=tournaments[1], position=2)
        Result.objects.create(friend=friend, tournament=tournaments[2], position=3)
        Result.objects.create(friend=friend, tournament=tournaments[3], position=4)
        Result.objects.create(friend=friend, tournament=tournaments[4], position=5)
        Result.objects.create(friend=friend, tournament=tournaments[5], position=1)
        self.assert_podiums(friend, [tournaments[5], tournaments[2], tournaments[1], tournaments[0]])

    def create_tournaments(self, amount):
        return [
            Tournament.objects.create(name=f'Tournament{i}',
                                      begin=date(day=i, month=1, year=2020),
                                      end=date(day=i, month=2, year=2020))
            for i in range(1, amount + 1)]

    def assert_podiums(self, friend, expected_tournaments):
        tournament_names = [result.tournament.name for result in podium_results(friend)]
        expected_tournament_names = [tournament.name for tournament in expected_tournaments]
        self.assertEqual(tournament_names, expected_tournament_names)

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
