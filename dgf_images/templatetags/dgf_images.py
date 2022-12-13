import logging
from datetime import datetime

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


def rating_update_from_current_month(current_rating):
    rating_date = current_rating.find('small', {'class': 'rating-date'})
    rating_update_month = datetime.strptime(rating_date.text, '(as of %d-%b-%Y)').month
    return rating_update_month == datetime.today().month


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
            if rating_difference and rating_update_from_current_month(current_rating):
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
    last = last_tournament(tour)
    parsed_results = [parse_friend_results(friend_results, friends_dict, tournaments, tour, last)
                      for friend_results in get_results(tour)]

    sorted_results = sorted(parsed_results,
                            key=lambda result: result["total_points"],
                            reverse=True)

    sorted_results_before = sorted(parsed_results,
                                   key=lambda result: result["total_points_before"],
                                   reverse=True)

    update_position_before(sorted_results, sorted_results_before)
    return sorted_results


def all_friends_dict():
    return {
        friend.id: friend
        for friend in Friend.all_objects.all()
    }


def get_results(tour):
    queryset = Result.objects.filter(tournament__tours=tour,
                                     division=tour.division,
                                     active=True) \
        .values('friend')
    for tournament in tour.tournaments.all():
        # This SUM contains actually JUST ONE element(the result of the Friend for the given Tournament)
        queryset = queryset.annotate(**{f'points_{tournament.id}': Sum('points', filter=Q(tournament=tournament))}) \
            .annotate(**{f'position_{tournament.id}': Sum('position', filter=Q(tournament=tournament))})
    return queryset


def parse_friend_results(friend_results, friends_dict, tournaments, tour, last_tournament):
    parsed_tournament_results = parse_tournaments(friend_results, tournaments)

    points = [result['points'] for result in parsed_tournament_results]
    sorted_points = sorted(points, reverse=True)

    points_before = [result['points'] for result in parsed_tournament_results if
                     result['tournament'].id != last_tournament.id]
    sorted_points_before = sorted(points_before, reverse=True)

    return {
        'friend': friends_dict[friend_results['friend']],
        'tournaments': parsed_tournament_results,
        'total_points': sum(sorted_points[:tour.evaluate_how_many]),
        'total_points_before': sum(sorted_points_before[:tour.evaluate_how_many])
    }


def parse_tournaments(friend_results, tournaments):
    parsed_tournaments = []
    for tournament in tournaments:
        parsed_tournament = parse_tournament(friend_results, tournament)
        if parsed_tournament['points'] is not None:
            parsed_tournaments.append(parsed_tournament)

    return parsed_tournaments


def parse_tournament(friend_results, tournament):
    return {
        'tournament': tournament,
        'position': friend_results[f'position_{tournament.id}'],
        'points': friend_results[f'points_{tournament.id}'],
    }


def update_position_before(results, results_before):
    position_before = {
        friend_results['friend'].id: position
        for position, friend_results in enumerate(results_before, start=1)
    }

    for position, friend_results in enumerate(results, start=1):
        friend_results['position'] = position
        friend_results['position_before'] = position_before[friend_results['friend'].id]


@register.filter
def last_tournament(tour):
    return tour.tournaments.annotate(results_count=Count('results')) \
        .filter(results_count__gt=0) \
        .order_by('begin') \
        .last()


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
def difference_string(value, value_before):
    difference = value - value_before
    if difference > 0:
        return f'+{difference}'
    elif difference < 0:
        return difference
    else:
        return ''


@register.filter
def difference_arrow_string(value, value_before):
    difference = value - value_before
    if difference > 0:
        return 'up'
    elif difference < 0:
        return 'down'
    else:
        return 'neutral'
