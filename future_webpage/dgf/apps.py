import csv
import logging

from django.apps import AppConfig
from django.conf import settings

from .models import Disc

logger = logging.getLogger(__name__)


def load_discs(filename):
    csv_reader = csv.reader(open(filename), delimiter=',')
    discs = dict()
    row_count = 0  # for skipping the header
    for row in csv_reader:
        if row_count != 0:
            # row[0] = manufacturer, row[1] = mold
            discs[row[1]] = row[0]
        row_count += 1
    logger.info('Loaded {} discs.'.format(row_count))
    return discs


def update_approved_discs(filename):
    loaded_discs = load_discs(filename)
    stored_discs = [x for x in Disc.objects.all().values_list('mold', flat=True)]

    for mold in loaded_discs.keys():
        if mold not in stored_discs:
            new_disc = Disc()
            new_disc.mold = mold
            new_disc.manufacturer = loaded_discs[mold]
            new_disc.save()


class DgfConfig(AppConfig):
    """
    This class loads once at the beginning (on startup).
    That's why it is good to have the update of the approved discs done here.
    """
    name = 'dgf'
    update_approved_discs(settings.PDGA_APPROVED_DISCS)
