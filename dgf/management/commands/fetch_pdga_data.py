import logging

from dgf import pdga
from dgf.management.base_dgf_command import BaseDgfCommand
from dgf.models import Friend
from dgf.pdga import PdgaApi

logger = logging.getLogger(__name__)


class Command(BaseDgfCommand):
    help = 'Updates Friend\'s rating and tournament information'

    def update_friend(self, pdga_api, friend, *args, **options):

        logger.info(f'Fetching PDGA data for {friend.username}...')

        try:
            pdga_api.update_friend_rating(friend)
            pdga_api.update_friend_tournament_statistics(friend)
            pdga.update_friend_tournaments(friend, pdga_api)

        except Exception as exception:
            if options['let_exceptions_raise']:
                raise exception
            else:
                self.handle_error(exception, friend=friend)

    def run(self, *args, **options):

        pdga_api = PdgaApi()

        for friend in Friend.objects.all():
            self.update_friend(pdga_api, friend, *args, **options)

        pdga_api.logout()
