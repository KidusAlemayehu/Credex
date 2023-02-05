from django.apps import AppConfig
from django.core.signals import request_finished
from . import signals

class FilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'files'

    def ready(self):
        request_finished.connect(signals.my_callback)