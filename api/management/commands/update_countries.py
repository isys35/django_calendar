from django.core.management.base import BaseCommand

from api.lib.parser_countries import parser_countries
from api.models import Country


class Command(BaseCommand):
    help = 'Parsing countries'

    def handle(self, *args, **options):
        print("[INFO] Update countries")
        countries_names = parser_countries()
        Country.objects.bulk_create([Country(name=name) for name in countries_names],
                                    ignore_conflicts=True)
        print("[INFO] Update finished")
