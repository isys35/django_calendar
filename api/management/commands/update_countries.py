from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
import requests


class Command(BaseCommand):
    help = 'Parsing countries'

    def handle(self, *args, **options):
        response = requests.get("https://www.officeholidays.com/countries")
        soup = BeautifulSoup(response.text, "lxml")
        countries_names = [el.text.strip() for el in soup.select('.four.omega.columns li a')]