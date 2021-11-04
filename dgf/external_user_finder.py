import logging

from django.utils.text import slugify

from dgf.models import Friend

logger = logging.getLogger(__name__)


def find_friend_by_metrix_user_id(metrix_user_id):
    if metrix_user_id is None:
        return None

    else:

        try:
            friend = Friend.all_objects.get(metrix_user_id=metrix_user_id)
            logger.info(f'Found Friend by Metrix User ID: {friend}')
            return friend

        except Friend.DoesNotExist:
            logger.info(f'Could not find Friend with Metrix User ID = "{metrix_user_id}"')
            return None


def find_friend_by_slugified_username(slugified_name):
    try:
        friend = Friend.all_objects.get(username=slugified_name)
        logger.info(f'Found Friend by slugified username: {friend}')
        return friend

    except Friend.DoesNotExist:
        logger.info(f'Could not find Friend with slugified username = "{slugified_name}"')
        return None


def find_friend_by_name(first_name, last_name):
    friends = Friend.all_objects.filter(first_name__icontains=first_name).filter(last_name__icontains=last_name)

    if friends.count() == 0:
        logger.info(f'Could not find Friend with first name = "{first_name}" and last name = "{last_name}"')
        return None

    if friends.count() == 1:
        friend = friends[0]
        logger.info(f'Found Friend by name: {friend}')
        return friend

    else:
        logger.info(f'Found more than one Friend with first name = "{first_name}" and last name = "{last_name}"')
        return None


def get_or_create_inactive_friend(metrix_user_id, slugified_name, first_name, last_name):
    """
    The Disc Golf Metrix user does not belong to the Disc Golf Friends.
    We do not want them to appear everywhere.
    Hence: is_active=False
    """

    friend = Friend.all_objects.create(username=slugified_name,
                                       slug=slugified_name,
                                       metrix_user_id=metrix_user_id,
                                       first_name=first_name,
                                       last_name=last_name,
                                       is_active=False
                                       )
    logger.info(f'Created Friend {friend}')
    return friend


def update_friend(friend, metrix_user_id, slugified_name, first_name, last_name):
    if not friend.is_active:
        if metrix_user_id:
            friend.metrix_user_id = metrix_user_id
        if slugified_name:
            friend.username = slugified_name
            friend.slug = slugified_name
        if first_name:
            friend.first_name = first_name
        if last_name:
            friend.last_name = last_name
        friend.save()
    return friend


def find_friend(metrix_user_id, name):
    slugified_name = slugify(name)
    names = name.split(' ')
    first_name = names[0]
    last_name = ' '.join(names[1:])

    friend = find_friend_by_metrix_user_id(metrix_user_id)
    if friend is not None:
        return update_friend(friend, metrix_user_id, slugified_name, first_name, last_name)

    friend = find_friend_by_slugified_username(slugified_name)
    if friend is not None:
        return update_friend(friend, metrix_user_id, slugified_name, first_name, last_name)

    friend = find_friend_by_name(first_name, last_name)
    if friend is not None:
        return update_friend(friend, metrix_user_id, slugified_name, first_name, last_name)

    return get_or_create_inactive_friend(metrix_user_id, slugified_name, first_name, last_name)
