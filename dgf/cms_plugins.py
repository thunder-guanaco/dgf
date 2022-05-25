import re
from datetime import datetime, timedelta

from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from djangocms_picture.models import Picture
from djangocms_picture.forms import PictureForm
from django.db.models import Count, Q, Max, OuterRef, Subquery
from django.utils.translation import gettext_lazy as _

import requests
from bs4 import BeautifulSoup

from .forms import TournamentResultForm
from .models import FriendPluginModel, Friend, CoursePluginModel, UdiscRound, Tournament, TourPluginModel, \
    BagTagChange, DiscGolfMetrixResultPluginModel
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


def friends_order_by_bag_tag():
    time_threshold = datetime.now() - timedelta(weeks=1)

    bag_tag_changes = BagTagChange.objects \
        .filter(previous_number__isnull=False) \
        .filter(active=True) \
        .filter(timestamp__gt=time_threshold) \
        .filter(friend=OuterRef('id')) \
        .order_by('-timestamp')

    return Friend.objects.filter(bag_tag__isnull=False) \
        .annotate(since=Max('bag_tag_changes__timestamp', filter=Q(bag_tag_changes__active=True))) \
        .annotate(previous_bag_tag=Subquery(bag_tag_changes.values_list('previous_number')[:1])) \
        .order_by('bag_tag')


def friends_without_bag_tag():
    return sorted(Friend.objects.filter(bag_tag__isnull=True), key=lambda f: f.short_name)


@plugin_pool.register_plugin
class TourResultsPluginPublisher(CMSPluginBase):
    model = TourPluginModel
    module = _('Disc Golf Friends')
    name = _('Tour Results')
    render_template = 'dgf/plugins/tour_results.html'


@plugin_pool.register_plugin
class BagTagsPagePluginPublisher(CMSPluginBase):
    model = CMSPlugin
    module = _('Disc Golf Friends')
    name = _('Bag Tags (whole page)')
    render_template = 'dgf/plugins/bag_tags_page.html'

    def render(self, context, instance, placeholder):
        context.update({
            'friends': friends_order_by_bag_tag(),
            'friends_without_bag_tag': friends_without_bag_tag(),
        })
        return context


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


@plugin_pool.register_plugin
class OnlyDesktopPluginPublisher(CMSPluginBase):
    model = CMSPlugin
    module = _('Disc Golf Friends Custom CMS')
    render_template = 'dgf/plugins/only_one_device.html'
    name = _('Only desktop')
    device = 'desktop'
    allow_children = True

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context.update({
            'device': self.device,
        })
        return context


@plugin_pool.register_plugin
class OnlyMobilePluginPublisher(OnlyDesktopPluginPublisher):
    name = _('Only mobile')
    device = 'mobile'


@plugin_pool.register_plugin
class DiscGolfFriendsFacebookPluginPublisher(CMSPluginBase):
    model = CMSPlugin
    module = _('Disc Golf Friends Facebook Pages')
    name = _('Facebook - Disc Golf Friends')
    render_template = 'dgf/plugins/facebook.html'
    page_id = 'discgolffriends'
    page_name = 'Disc Golf Friends'

    def render(self, context, instance, placeholder):
        context.update({
            'page_id': self.page_id,
            'page_name': self.page_name,
        })
        return context


@plugin_pool.register_plugin
class TremoniaOpenFacebookPluginPublisher(DiscGolfFriendsFacebookPluginPublisher):
    name = _('Facebook - Tremonia Open')
    page_id = 'tremoniaopen'
    page_name = 'Tremonia Open'



def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, features='html5lib')


def get_results_tables(soup, is_tremoria_series):
    table = soup.find('table')
    amateur_tr = table.find('th', text=re.compile('.*Amateur.*')).parent
    previous_tds = reversed(list(amateur_tr.previous_siblings))

    return {
        'results_header': table.find('thead').prettify(),
        'results_open': '\n'.join([tag.prettify() for tag in previous_tds if 'Open' not in tag.prettify()]),
        'results_amateur': '\n'.join([tag.prettify() for tag in amateur_tr.next_siblings]),
    }


def get_title(soup):
    return soup.find('head').find('title').text.split('→')[1]


@plugin_pool.register_plugin
class TremoniaSeriesLastTournamentResultsPluginPublisher(CMSPluginBase):
    model = DiscGolfMetrixResultPluginModel
    module = _('Social Media')
    name = _('Tournament Results')
    render_template = 'dgf/plugins/tournament_results_for_social_media.html'

    def render(self, context, instance, placeholder):
        soup = get_soup(instance.url)
        title = get_title(soup)
        context.update({
            'background_image': instance.background_image,
            'title': title,
        })
        context.update(get_results_tables(soup, 'Tremonia Series' in title))
        return context
