import logging

from django import template
from django.core.cache import cache

from dgf.models import Friend
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
            rating_difference = current_rating.find("a", {"class": "rating-difference"})
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
    Usage `{{ "aaa"|replace:"a|b" }}`
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
    Usage `{{ request|mobile_or_desktop:"25|50" }}`
    """
    values = arg.split('|')
    if len(values) != 2:
        raise ValueError('Unexpected value. Expected something like "25|50"')

    mobile, desktop = values
    return mobile if request.user_agent.is_mobile else desktop
