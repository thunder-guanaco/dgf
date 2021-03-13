import logging

from django.apps import AppConfig
from django.core.cache import cache

logger = logging.getLogger(__name__)


class DgfConfig(AppConfig):
    name = 'dgf'
    verbose_name = 'Disc Golf Friends'

    def get_all_objects(self, model_class, order_by):
        return [('', '---')] + [(x.id, str(x)) for x in
                                model_class.objects.all().order_by(order_by)]

    def ready(self):
        Disc = self.get_model('Disc')
        Course = self.get_model('Course')

        cache.set('ALL_DISCS', self.get_all_objects(Disc, 'mold'))
        logger.info('Loaded all discs from DB into the cache')

        cache.set('ALL_COURSES', self.get_all_objects(Course, 'name'))
        logger.info('Loaded all courses from DB into the cache')
