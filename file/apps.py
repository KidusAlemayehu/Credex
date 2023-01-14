from django.apps import AppConfig
from django.core.signals import request_finished
from . import signals

class FileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'file'

    def ready(self):
        request_finished.connect(signals.my_callback)