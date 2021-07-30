from django.apps import AppConfig


class Datamad2Config(AppConfig):
    name = 'datamad2'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import datamad2.signals
