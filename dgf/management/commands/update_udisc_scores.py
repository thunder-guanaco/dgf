import logging

from django.core.management.base import BaseCommand

from dgf.management import error_handler
from dgf.models import CoursePluginModel, UdiscRound
from dgf.udisc import update_udisc_scores

logger = logging.getLogger(__name__)

RETRIES = 5


class Command(BaseCommand):
    help = 'Updates all UDisc scores for the courses that have a plugin associated to them'

    def update_scores(self, course):
        update_udisc_scores(course)
        return UdiscRound.objects.filter(course=course).count()

    def update_all_scores(self):

        all_plugins = CoursePluginModel.objects.all()
        count = all_plugins.count()
        if count == 0:
            logger.warning('No courses to update')
            return

        logger.info(f'Updating {count} courses')

        for plugin in all_plugins:

            course = plugin.course

            for i in range(RETRIES):

                logger.info(f'({i + 1}/{RETRIES}) Trying to update scores for {course}')

                try:
                    amount_of_new_rounds = self.update_scores(course)
                    # Everything went well. No need to retry
                    logger.info(f'Successfully updated {amount_of_new_rounds} scores for course "{course}"\n')
                    break

                except UserWarning as w:
                    # It's impossible to fix this. The user has to do something
                    logger.error(w)
                    raise w

                except Exception as e:
                    # This could always happen because you never know with Selenium
                    logger.warning(e)
                    continue
            else:
                raise UserWarning(f'Could not update course {course}')

    def handle(self, *args, **options):

        try:
            self.update_all_scores()

        except Exception as e:
            error_handler.handle(self, e)
