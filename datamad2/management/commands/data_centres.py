from django.core.management.base import BaseCommand, CommandError
from datamad2.models import DataCentre
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = __doc__

    def handle(self, *args, **options):

        dcs = ["BODC", "CEDA", "EIDC", "NGDC", "PDC", "ADS"]
        for dc in dcs:
            try:
                DataCentre.objects.get(name=dc)
            except ObjectDoesNotExist:
                DataCentre.objects.create(name=dc)
