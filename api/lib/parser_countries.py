import requests
from bs4 import BeautifulSoup


def parser_countries():
    response = requests.get("https://www.officeholidays.com/countries")
    soup = BeautifulSoup(response.text, "lxml")
    countries = [el.text.strip() for el in soup.select('.four.omega.columns li a')]
    return countries