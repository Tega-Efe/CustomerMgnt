from django.apps import AppConfig


class MgntappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mgntApp'

    def ready(self):
        import mgntApp.signals
