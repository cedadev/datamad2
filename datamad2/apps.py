from django.apps import AppConfig


class Datamad2Config(AppConfig):
    name = 'datamad2'

    def ready(self):
        import datamad2.signals
