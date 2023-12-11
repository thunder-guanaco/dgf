import logging
import traceback
from abc import abstractmethod, ABC

from django.core.management.base import BaseCommand

from dgf.models import GitHubIssue

logger = logging.getLogger(__name__)


def extract_exception_name(exception):
    return type(exception).__name__


class BaseDgfCommand(BaseCommand, ABC):

    @abstractmethod
    def run(self, *args, **options):
        ...

    def add_arguments(self, parser):
        parser.add_argument(
            '--let-exceptions-raise',
            action='store_true',
            help='Do not handle exceptions and raise them (for example when for calling from admin)',
        )

    def handle(self, *args, **options):

        logger.info(f'>>> Running {self.__module__}...')

        try:
            self.run(*args, **options)

        except Exception as exception:
            if options['let_exceptions_raise']:
                raise exception
            else:
                self.handle_error(exception)

        logger.info(f'>>> {self.__module__} DONE')

    def handle_error(self, exception, friend=None):
        exception_name = extract_exception_name(exception)

        friend_msg = f'Exception while updating {friend}' if friend else 'Exception'
        error_msg = f'{exception_name} while executing management command: {self.__module__}'

        exception_args_str = '\n'.join([f'* {arg}' for arg in exception.args])
        traceback_str = '\n'.join(traceback.format_exception(exception))

        logger.exception(f'{friend_msg}: {error_msg}')
        GitHubIssue.objects.create(title=error_msg,
                                   body=f'# {exception_name}\n{exception_args_str}\n'
                                        f'# Traceback\n```{traceback_str}```',
                                   friend=friend,
                                   type=GitHubIssue.MANAGEMENT_COMMAND_ERROR)
