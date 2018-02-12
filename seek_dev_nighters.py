import requests
from pytz import timezone
from datetime import datetime


def load_attempts():
    page_number = 1
    while True:
        page_content = load_page_content(page_number)
        if not page_content:
            break
        for record in page_content['records']:
            yield record
        page_number += 1


def get_midnighters(attempts):
    night_hours_start = 0
    night_hours_end = 6
    midnighters = set()
    for attempt in attempts:
        hour_of_attempt = datetime.fromtimestamp(attempt['timestamp'], timezone(attempt['timezone'])).hour
        if (night_hours_start <= hour_of_attempt < night_hours_end):
            midnighters.add(attempt['username'])
    return midnighters


def load_page_content(page):
    url = 'https://devman.org/api/challenges/solution_attempts/'
    response = requests.get(url, params={'page': page})
    if response:
        return response.json()


def print_midnighters(midnighters):
    print('Devman midnighters:')
    for username in midnighters:
        print(username)


if __name__ == '__main__':
    try:
        midnighters = get_midnighters(load_attempts())
    except requests.HTTPError as error:
        print('HTTP Error!')
        print('Response is: {0}'.format(error.response.content))
    except requests.ConnectionError:
        print('Connection failed!')
    if midnighters:
        print_midnighters(midnighters)
    else:
        print('Devman does not have midnighters')
