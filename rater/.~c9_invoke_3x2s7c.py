""" app configs """
from django.apps import AppConfig


class RaterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rater'

    def ready(self):
        """ import signals """
        import rater.signals
