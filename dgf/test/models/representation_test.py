from django.test import TestCase
from parameterized import parameterized

from dgf.models import Division, FavoriteCourse, CoursePluginModel, FriendPluginModel, Friend, Course, UdiscRound, \
    Highlight, Video, Attendance
from .creator import create_friends, create_courses, create_tournaments


class ModelRepresentationTest(TestCase):

    def test_division_representation(self):
        division = Division(id='MPO', text='MPO - Pro Open')
        self.assertEqual(str(division), division.text)

        division = Division(id='MJ1')
        self.assertEqual(str(division), division.id)

    def test_udisc_round_representation(self):
        udisc_round = UdiscRound(friend=create_friends(1), course=create_courses(1), score=50)
        self.assertEqual(str(udisc_round), 'Friend0 scored 50 in Course0')

    def test_favorite_course_representation(self):
        favorite_course = FavoriteCourse(friend=create_friends(1), course=create_courses(1))
        self.assertEqual(str(favorite_course), 'Course0')

    def test_highlight_representation(self):
        highlight = Highlight(content='highlight', friend=create_friends(1))
        self.assertEqual(str(highlight), 'highlight')

    def test_video_representation(self):
        video = Video(url='youtube.com/asd', type=Video.OTHER, friend=create_friends(1))
        self.assertEqual(str(video), 'youtube.com/asd')

    def test_attendance_representation(self):
        attendance = Attendance(friend=create_friends(1), tournament=create_tournaments(1))
        self.assertEqual(str(attendance), 'Friend0 will attend Tournament0 (01. Jan 2020)')

    @parameterized.expand([
        ('Course', CoursePluginModel, Course, 'name',),
        ('Friend', FriendPluginModel, Friend, 'username',),
    ])
    def test_plugin_model_representation(self, model_name, plugin_class, model_class, model_field):
        model_instance = model_class(**{model_field: 'test'})
        plugin_instance = plugin_class(**{model_name.lower(): model_instance})
        self.assertEqual(str(plugin_instance), f'{model_name} plugin for {str(model_instance)}')
