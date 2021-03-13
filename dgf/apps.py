import logging

from django.apps import AppConfig
from django.core.cache import cache

from dgf.models import Disc, Course

logger = logging.getLogger(__name__)


class DgfConfig(AppConfig):
    name = 'dgf'

    def get_all_objects(self, model_class):
        return [('', '---')] + [(x.id, str(x)) for x in
                                model_class.objects.all().order_by('id')]

    def ready(self):
        cache.set('ALL_DISCS', self.get_all_objects(Disc))
        logger.info('Loaded all discs from DB into the cache')

        cache.set('ALL_COURSES', self.get_all_objects(Course))
        logger.info('Loaded all courses from DB into the cache')
