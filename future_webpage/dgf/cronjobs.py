import logging

from .models import Friend
from .pdga import PdgaApi

logger = logging.getLogger(__name__)


def fetch_rating():
    pdga_service = PdgaApi()
    for friend in Friend.objects.all():
        if friend.pdga_number:
            pdga_friend_response = pdga_service.query_player(pdga_number=friend.pdga_number)
            friend.rating = int(pdga_friend_response['players'][0]['rating'])
            friend.save()
            logger.info('{} has now rating: {}'.format(friend.username, friend.rating))
