import logging

from django.core import management
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Backups DB and media'

    def handle(self, *args, **options):
        logger.info('Starting back up...')

        management.call_command('dbbackup')
        logger.info('Database backup has been completed')

        management.call_command('mediabackup')
        logger.info('Media backup has been completed')
