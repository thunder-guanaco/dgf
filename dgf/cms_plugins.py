from datetime import datetime

from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.db.models import Count, Q
from django.utils.translation import ugettext as _

from .models import FriendPluginModel, Friend, CoursePluginModel, UdiscRound, Tournament
from .udisc import get_course_url


@plugin_pool.register_plugin
class FriendPluginPublisher(CMSPluginBase):
    model = FriendPluginModel
    module = _('Disc Golf Friends')
    name = _('Friend')
    render_template = 'dgf/plugins/friend.html'
    zoom = '1'

    def render(self, context, instance, placeholder):
        context.update({
            'friend': instance.friend,
            'zoom': self.zoom,
        })
        return context


@plugin_pool.register_plugin
class SmallerFriendPluginPublisher(FriendPluginPublisher):
    name = _('Friend (small)')
    zoom = '0.5'


@plugin_pool.register_plugin
class BiggerFriendPluginPublisher(FriendPluginPublisher):
    name = _('Friend (big)')
    zoom = '2'


@plugin_pool.register_plugin
class FriendsHeaderPluginPublisher(CMSPluginBase):
    model = CMSPlugin
    module = _('Disc Golf Friends')
    name = _('Friends Header')
    render_template = 'dgf/plugins/friends_header.html'

    def render(self, context, instance, placeholder):
        context.update({'friends': Friend.objects.all().order_by('?')})
        return context


@plugin_pool.register_plugin
class UdiscPluginPublisher(CMSPluginBase):
    model = CoursePluginModel
    module = _('Disc Golf Friends')
    name = _('UDisc Best Scores')
    render_template = 'dgf/plugins/udisc.html'

    def render(self, context, instance, placeholder):
        course = instance.course
        context.update({
            'course_url': get_course_url(course),
            'rounds': UdiscRound.objects.filter(course=course).order_by('score'),
            'course': course,
        })
        return context


@plugin_pool.register_plugin
class GoogleCalendarPluginPublisher(CMSPluginBase):
    model = CMSPlugin
    module = _('Disc Golf Friends')
    name = _('Disc Golf Friends Calendar')
    render_template = 'dgf/plugins/calendar.html'


def friends_order_by_ts_wins():
    return Friend.all_objects.filter(results__tournament__name__startswith='Tremonia Series',
                                     results__position__in=[1, 2, 3]) \
        .annotate(ts_wins=Count('results__position', filter=Q(results__position=1))) \
        .annotate(ts_seconds=Count('results__position', filter=Q(results__position=2))) \
        .annotate(ts_thirds=Count('results__position', filter=Q(results__position=3))) \
        .order_by('-ts_wins', '-ts_seconds', '-ts_thirds')


@plugin_pool.register_plugin
class TremoniaSeriesHallOfFamePluginPublisher(CMSPluginBase):
    model = CMSPlugin
    module = _('Tremonia Series')
    name = _('Hall Of Fame (small)')
    render_template = 'dgf/plugins/tremonia_series_hall_of_fame.html'

    def render(self, context, instance, placeholder):
        context.update({
            'friends': friends_order_by_ts_wins(),
        })
        return context


@plugin_pool.register_plugin
class TremoniaSeriesHallOfFamePagePluginPublisher(CMSPluginBase):
    model = CMSPlugin
    module = _('Tremonia Series')
    name = _('Hall Of Fame (whole page)')
    render_template = 'dgf/plugins/tremonia_series_hall_of_fame_page.html'

    def render(self, context, instance, placeholder):
        context.update({
            'friends': friends_order_by_ts_wins(),
        })
        return context


@plugin_pool.register_plugin
class TremoniaSeriesNextTournamentsPluginPublisher(CMSPluginBase):
    model = CMSPlugin
    module = _('Tremonia Series')
    name = _('Next Tournaments')
    render_template = 'dgf/plugins/tremonia_series_next_tournaments.html'

    def render(self, context, instance, placeholder):
        context.update({
            'tournaments': Tournament.objects.filter(name__startswith='Tremonia Series').filter(
                begin__gte=datetime.today()).order_by('begin'),
        })
        return context
