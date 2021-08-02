from datetime import datetime

import requests
from ics import Calendar
from tatsu.exceptions import FailedParse

from api.lib.parser_countries import parser_countries


def parser_holidays(country: str):
    url = f'https://www.officeholidays.com/ics/ics_country.php?tbl_country={country}'
    try:
        calendar = Calendar(requests.get(url).text)
    except FailedParse:
        return []
    holidays = []
    for event in calendar.events:
        event_name = event.name.replace(f"{country}: ", "")
        event_date = datetime.strptime(str(event.begin), "%Y-%m-%dT%H:%M:00+00:00")
        holidays.append((event_name, event_date))
    return holidays


if __name__ == '__main__':
    countries = parser_countries()
    for country in parser_countries():
        for event_name, event_date in parser_holidays(country):
            print(event_name, event_date)
