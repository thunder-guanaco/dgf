from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _

from .models import FriendPluginModel, Friend, CoursePluginModel, UdiscRound
from .udisc import get_course_url


@plugin_pool.register_plugin
class FriendPluginPublisher(CMSPluginBase):
    model = FriendPluginModel
    module = _('Disc Golf Friends')
    name = _('Friend')
    render_template = 'dgf/friend_plugin.html'
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
    render_template = 'dgf/friends_header.html'

    def render(self, context, instance, placeholder):
        context.update({'friends': Friend.objects.all().order_by('?')})
        return context


@plugin_pool.register_plugin
class UdiscPluginPublisher(CMSPluginBase):
    model = CoursePluginModel
    module = _('Disc Golf Friends')
    name = _('UDisc Best Scores')
    render_template = 'dgf/udisc.html'

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
    render_template = 'dgf/friends_calendar.html'


@plugin_pool.register_plugin
class TremoniaSeriesHallOfFamePluginPublisher(CMSPluginBase):
    model = CMSPlugin
    module = _('Disc Golf Friends')
    name = _('Tremonia Series - Hall Of Fame')
    render_template = 'dgf/plugins/tremonia_series_hall_of_fame.html'

    def render(self, context, instance, placeholder):
        context.update({
            'friends': Friend.objects.all(),
        })
        return context
