from datetime import datetime

from django.core.management.base import BaseCommand

from api.lib.parser_holidays import parser_holidays
from api.models import Country, Holiday, CountryHoliday


class Command(BaseCommand):
    help = 'Parsing countries'

    def handle(self, *args, **options):
        print("[INFO] Update holidays")
        for country in Country.objects.all():
            holidays_typles = parser_holidays(country.name)
            Holiday.objects.bulk_create([Holiday(name=el[0]) for el in holidays_typles], ignore_conflicts=True)
            CountryHoliday.objects.bulk_create(
                [CountryHoliday(holiday_id=el[0],
                                country_id=country.name,
                                date=el[1]) for el in holidays_typles]
            , ignore_conflicts=True)
        print("[INFO] Update finished")