import requests
from pytz import timezone
from datetime import datetime

URL = 'https://devman.org/api/challenges/solution_attempts/'
NIGHT_HOURS_START = 0
NIGHT_HOURS_END = 6


def load_attempts():
    first_page_number = 1
    first_page_content = load_page_content(first_page_number)
    if first_page_content:
        pages = first_page_content['number_of_pages']
    else:
        return []
    for page in range(1, pages):
        for record in load_page_content(page)['records']:
            yield record


def get_midnighters():
    midnighters = []
    for attempt in load_attempts():
        if attempt['timestamp']:
            attempt_date = datetime.fromtimestamp(float(attempt['timestamp']))
            hour_of_attempt = timezone(attempt['timezone']).fromutc(attempt_date).hour
            if hour_of_attempt >= NIGHT_HOURS_START and hour_of_attempt < NIGHT_HOURS_END:
                attempt['time'] = str(hour_of_attempt)
                midnighters.append(attempt['username'])
    return set(midnighters)


def load_page_content(page):
    return requests.get(URL, params={'page': page}).json()


def print_midnighters():
    try:
        midnighters = get_midnighters()
        if midnighters:
            print('Devman midnighters:')
        else:
            print('Devman does not have midnighters')
        for username in midnighters:
            print(username)
    except requests.HTTPError as error:
        print('HTTP Error!')
        print('Response is: {0}'.format(error.response.content))
    except requests.ConnectionError:
        print('Connection failed!')


if __name__ == '__main__':
    print_midnighters()
