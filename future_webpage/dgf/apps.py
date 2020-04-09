import csv
import logging
import os

from django.apps import AppConfig

from .models import Disc

logger = logging.getLogger(__name__)


def load_discs():
    script_dir = os.path.dirname(__file__)
    join = os.path.join(script_dir, './resources/pdga-approved-disc-golf-discs.csv')
    csv_reader = csv.reader(open(join), delimiter=',')
    discs = dict()
    row_count = 0  # for skipping the header
    for row in csv_reader:
        if row_count != 0:
            # row[0] = manufacturer, row[1] = mold
            discs[row[1]] = row[0]
        row_count += 1
    logger.info('Loaded {} discs.'.format(row_count))
    return discs


def update_approved_discs():
    loaded_discs = load_discs()
    stored_discs = Disc.objects.all()
    all_stored_molds = []

    # mold names are unique
    for disc in stored_discs:
        all_stored_molds.append(disc.mold)

    for mold in loaded_discs.keys():
        if mold not in all_stored_molds:
            new_disc = Disc()
            new_disc.mold = mold
            new_disc.manufacturer = loaded_discs[mold]
            new_disc.save()
            logger.info('New mold was found: {}'.format(new_disc))


class DgfConfig(AppConfig):
    """
    This class loads once at the beginning (on startup).
    That's why it is good to have the update of the approved discs done here.
    """
    name = 'dgf'
    update_approved_discs()

    def ready(self):
        pass
