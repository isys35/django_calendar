from datetime import datetime

import requests
from ics import Calendar


def parser_holidays(country: str):
    url = f'https://www.officeholidays.com/ics/ics_country.php?tbl_country={country}'
    calendar = Calendar(requests.get(url).text)
    for event in calendar.events:
        event_name = event.name.replace(f"{country}: ", "")
        event_date = datetime.strptime(str(event.begin), "%Y-%m-%dT%H:%M:00+00:00")
        yield event_name, event_date


if __name__ == '__main__':
    for event_name, event_date in parser_holidays("Albania"):
        print(event_name, event_date)
