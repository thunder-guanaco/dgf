import logging

from dgf.models import Feedback

logger = logging.getLogger(__name__)


def handle(command, exception, friend=None):
    command_class = type(command)
    command_class_name = f'{command_class.__module__}.{command_class.__name__}'

    friend_msg = f'Exception while updating {friend}' if friend else ''
    error_msg = f'Error while executing management command: {command_class_name}'

    exception_args_str = '\n'.join([f'* {arg}' for arg in exception.args])

    logger.exception(f'{friend_msg} {error_msg}')
    Feedback.objects.create(title=error_msg,
                            feedback=f'# {type(exception).__name__}\n{exception_args_str}',
                            friend=friend)
