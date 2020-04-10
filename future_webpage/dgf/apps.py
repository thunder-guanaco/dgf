from django.apps import AppConfig


class DgfConfig(AppConfig):
    """
    This class loads once at the beginning (on startup).
    That's why it is good to have the update of the approved discs done here.
    """
    name = 'dgf'
