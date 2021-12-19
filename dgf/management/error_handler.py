from dgf.models import Feedback


def handle(command, exception):
    command_class = type(command)
    command_class_name = f'{command_class.__module__}.{command_class.__name__}'

    exception_args_str = '\n'.join([f'* {arg}' for arg in exception.args])

    Feedback.objects.create(title=f'Error while executing management command: {command_class_name}',
                            feedback=f'# {type(exception).__name__}\n{exception_args_str}',
                            friend=None)
