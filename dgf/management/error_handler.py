import logging
import traceback

from dgf.models import GitHubIssue

logger = logging.getLogger(__name__)


def handle(command, exception, friend=None):
    command_class = type(command)
    command_class_name = f'{command_class.__module__}.{command_class.__name__}'

    exception_name = type(exception).__name__

    friend_msg = f'Exception while updating {friend}' if friend else 'Exception'
    error_msg = f'{exception_name} while executing management command: {command_class_name}'

    exception_args_str = '\n'.join([f'* {arg}' for arg in exception.args])
    traceback_str = '\n'.join(traceback.format_exception(exception))

    logger.exception(f'{friend_msg}: {error_msg}')
    GitHubIssue.objects.create(title=error_msg,
                               body=f'# {exception_name}\n{exception_args_str}\n'
                                    f'# Traceback\n```{traceback_str}```',
                               friend=friend,
                               type=GitHubIssue.MANAGEMENT_COMMAND_ERROR)
