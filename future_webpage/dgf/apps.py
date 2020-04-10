import csv
import logging

from django.apps import AppConfig
from django.conf import settings

from .models import Disc

logger = logging.getLogger(__name__)


def load_discs(approved_discs):
    csv_reader = csv.reader(approved_discs, delimiter=',')
    discs = dict()
    count = 0
    for row in csv_reader:
        if count != 0:
            # row[0] = manufacturer, row[1] = mold
            discs[row[1]] = row[0]
        count += 1
    logger.info('Loaded {} discs.'.format(count))
    return discs


def update_approved_discs(approved_discs):
    loaded_discs = load_discs(approved_discs)
    stored_discs = [x for x in Disc.objects.all().values_list('mold', flat=True)]

    for mold in loaded_discs.keys():
        if mold not in stored_discs:
            new_disc = Disc()
            new_disc.mold = mold
            new_disc.manufacturer = loaded_discs[mold]
            logger.info('saving: {} - {}'.format(new_disc.mold, new_disc.manufacturer))
            new_disc.save()


class DgfConfig(AppConfig):
    """
    This class loads once at the beginning (on startup).
    That's why it is good to have the update of the approved discs done here.
    """
    name = 'dgf'
    update_approved_discs(open(settings.PDGA_APPROVED_DISCS))
