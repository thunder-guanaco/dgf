from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.db.models import Count, Q, Max, Min, Avg, OuterRef, Subquery
from django.utils.translation import gettext_lazy as _

from . import tremonia_series
from .models import Friend, UdiscRound, Tournament, BagTagChange
from .plugin_models import FriendPluginModel, CoursePluginModel, TourPluginModel, \
    ConcreteTournamentResultsPluginModel, LastTremoniaSeriesResultsPluginModel
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
        .filter(active=True) \
        .filter(previous_number__isnull=False) \
        .filter(timestamp__gt=time_threshold) \
        .filter(friend=OuterRef('id')) \
        .order_by('-timestamp')

    bag_tag_changes_grouped_by_number = BagTagChange.objects \
        .filter(friend=OuterRef('id')) \
        .values('new_number') \
        .annotate(amount=Count('new_number')) \
        .order_by('-amount', 'new_number')

    return Friend.objects.filter(bag_tag__isnull=False) \
        .annotate(previous_bag_tag=Subquery(bag_tag_changes.values_list('previous_number')[:1])) \
        .annotate(since=Max('bag_tag_changes__timestamp',
                            filter=Q(bag_tag_changes__active=True))) \
        .annotate(bag_tag_changes_count=Count('bag_tag_changes',
                                              filter=Q(bag_tag_changes__previous_number__isnull=False))) \
        .annotate(first_bag_tag_change=Min('bag_tag_changes__timestamp')) \
        .annotate(best_bag_tag=Min('bag_tag_changes__new_number')) \
        .annotate(worst_bag_tag=Max('bag_tag_changes__new_number')) \
        .annotate(average_bag_tag=Avg('bag_tag_changes__new_number')) \
        .annotate(most_received_bag_tag=Subquery(bag_tag_changes_grouped_by_number.values_list('new_number')[:1])) \
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
            'tournaments': tremonia_series.next_tournaments(),
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


@plugin_pool.register_plugin
class ConcreteTournamentResultsPluginPublisher(CMSPluginBase):
    model = ConcreteTournamentResultsPluginModel
    module = _('Social Media')
    name = _('Concrete Tournament Results')
    render_template = 'dgf/plugins/social_media/concrete_tournament_results.html'

    def render(self, context, instance, placeholder):

        if not instance.tournament:
            instance.tournament = Tournament.objects \
                .filter(end__lte=datetime.today()) \
                .order_by('-end') \
                .first()

        return super().render(context, instance, placeholder)


@plugin_pool.register_plugin
class LastTremoniaSeriesResultsPluginPublisher(CMSPluginBase):
    model = LastTremoniaSeriesResultsPluginModel
    module = _('Social Media')
    name = _('Last Tremonia Series Results')
    render_template = 'dgf/plugins/social_media/last_tremonia_series_results.html'

    def render(self, context, instance, placeholder):
        last_ts = Tournament.objects.filter(name__startswith='Tremonia Series') \
            .filter(end__lte=datetime.today()) \
            .order_by('-end') \
            .first()
        soup = self.get_soup(last_ts.url)
        title = self.get_title(soup)
        context.update({
            'instance': instance,
            'title': title,
        })

        try:
            context.update(self.get_results_from_manual_results_table(soup))
        except Exception:
            context.update({'manual_table_error': True})
            context.update(self.get_results_from_default_results_table_with_different_courses(soup))

        return context

    def get_soup(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.content, features='html5lib')

    def get_title(self, soup):
        title = soup.find('head').find('title').text
        if '→' in title:
            return title.split('→')[1]
        else:
            return title

    def get_results_from_manual_results_table(self, soup):
        table = soup.find('table')
        header = table.find('thead')
        body = table.find('tbody')
        divisions = []
        for tr in body.find_all('tr'):
            if tr.find('th'):
                divisions.append({
                    'name': tr.find_all("th")[1].text,
                    'results': [],
                })
            else:
                divisions[-1]['results'].append(tr.prettify())

        return {
            'results_header': header.prettify(),
            'results_body': divisions,
        }

    def get_results_from_default_results_table_with_different_courses(self, soup):
        table = soup.find("table", {"class": "score-table"})
        headers = table.find_all('thead')
        bodies = table.find_all('tbody')
        divisions = []
        division_names = []
        for head in headers[1:]:
            division_names.append(head.find("tr").find_all("th")[1].text.split(" (")[0])

        for division_names, tbody in zip(division_names, bodies):
            divisions.append({
                'name': division_names,
                'results': [tr.prettify for tr in tbody.find_all('tr')],
            })

        return {
            'results_header': headers[0].prettify(),
            'results_body': divisions,
        }
