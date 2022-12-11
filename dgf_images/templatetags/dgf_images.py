import logging

from django import template
from django.core.cache import cache
from django.db.models import Count, Q, Sum

from dgf.models import Friend, Tour, Result
from dgf.pdga.common import get_player_page

register = template.Library()

logger = logging.getLogger(__name__)


@register.simple_tag
def all_friends():
    return Friend.objects \
        .filter(social_media_agreement=True) \
        .exclude(main_photo__isnull=True) \
        .exclude(main_photo='') \
        .order_by('?')


@register.simple_tag
def all_friends_dict():
    return {
        friend.id: friend
        for friend in Friend.all_objects.all()
    }


def get_rating_difference(friends):
    for friend in friends:
        rating_check = cache.get(f'rating_check_{friend.username}')
        # rating_check is either:
        #    None: there are no records of that friend
        #    False: Friend was already checked and there's no rating difference
        #    True: Friend was already checked and there are rating and raring difference

        if rating_check is not None:
            if not rating_check:
                continue
            friend.rating_difference = cache.get(f'rating_difference_{friend.username}')
            friend.rating = cache.get(f'rating_{friend.username}')
            yield friend
            continue

        player_page_soup = get_player_page(friend.pdga_number)
        current_rating = player_page_soup.find('li', {'class': 'current-rating'})
        if current_rating:
            rating_difference = current_rating.find('a', {'class': 'rating-difference'})
            if rating_difference:
                friend.rating_difference = rating_difference.text
                friend.rating = [child.text.strip() for child in current_rating.children
                                 if not child.name and child.text.strip()][0]
                cache.set(f'rating_difference_{friend.username}', friend.rating_difference, 60 * 60 * 24)
                cache.set(f'rating_{friend.username}', friend.rating, 60 * 60 * 24)
                cache.set(f'rating_check_{friend.username}', True, 60 * 60 * 24)
                yield friend
                continue
        cache.set(f'rating_check_{friend.username}', False, 60 * 60 * 24)


@register.simple_tag
def all_tours():
    return Tour.objects.all().order_by('-name')


@register.filter
def parse_results(tour):
    tournaments = tour.tournaments.all().order_by('begin')
    friends_dict = all_friends_dict()
    return [parse_friend_results(friend_results, friends_dict, tournaments) for friend_results in get_results(tour)]


def parse_friend_results(friend_results, friends_dict, tournaments):
    return {
        'friend': friends_dict[friend_results['friend']],
        'tournaments': [parse_tournament(tournament, friend_results) for tournament in tournaments]
    }


def parse_tournament(tournament, friend_results):
    return {
        'tournament': tournament,
        'position': friend_results[f'position_{tournament.id}'],
        'points': friend_results[f'points_{tournament.id}'],
    }


def get_results(tour):
    queryset = Result.objects.filter(tournament__tours=tour).values('friend')
    for tournament in tour.tournaments.all():
        # This SUM contains actually JUST ONE element(the result of the Friend for the given Tournament)
        queryset = queryset.annotate(**{f'points_{tournament.id}': Sum('points', filter=Q(tournament=tournament))}) \
            .annotate(**{f'position_{tournament.id}': Sum('position', filter=Q(tournament=tournament))})
    return queryset


@register.filter
def sorted_tour_points(result):
    points = [
        value
        for key, value in result.items()
        if key.startswith('points_') and value is not None
    ]
    return sorted(points, reverse=True)


@register.filter
def sorted_tour_points_without_tournament(result, tournament):
    points = [
        value
        for key, value in result.items()
        if key.startswith('points_') and key != f'points_{tournament.id}' and value is not None
    ]
    return sorted(points, reverse=True)


@register.filter
def last_tournament(tour):
    return tour.tournaments.annotate(results_count=Count('results')) \
        .filter(results_count__gt=0) \
        .order_by('begin') \
        .last()


@register.filter
def points_from_tournament(results, tournament):
    return results[f"points_{tournament.id}"] or '-'


@register.filter
def position_from_tournament(results, tournament):
    return results[f"position_{tournament.id}"]


@register.simple_tag
def all_pdga_friends():
    friends = Friend.objects \
        .filter(social_media_agreement=True) \
        .exclude(pdga_number__isnull=True) \
        .exclude(rating__isnull=True) \
        .exclude(main_photo__isnull=True) \
        .exclude(main_photo='')

    friends = get_rating_difference(friends)
    return sorted(friends, key=lambda friend: -int(friend.rating_difference))


@register.filter
def replace(value, arg):
    """
    Replace characters inside string
    Usage `{{ 'aaa'|replace:'a|b' }}`
    """
    replacement = arg.split('|')
    if len(replacement) != 2:
        return value

    what, to = replacement
    return value.replace(what, to)


@register.filter
def mobile_or_desktop(request, arg):
    """
    Returns first value if mobile and the second if desktop
    Usage `{{ request|mobile_or_desktop:'25|50' }}`
    """
    values = arg.split('|')
    if len(values) != 2:
        raise ValueError('Unexpected value. Expected something like "25|50"')

    mobile, desktop = values
    return mobile if request.user_agent.is_mobile else desktop


@register.filter
def sum_all(iterable):
    return sum(iterable)


@register.filter
def get(dict, key):
    return dict[key]


@register.filter
def difference_text(value, value_before):
    result = value - value_before
    return f'+{result}' if result > 0 else ''
