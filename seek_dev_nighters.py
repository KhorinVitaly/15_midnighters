import requests
from pytz import timezone
from datetime import datetime, time

URL = 'https://devman.org/api/challenges/solution_attempts/'
NIGHT_TIME = {'start': time(0, 0, 0, 0, None),
              'end': time(6, 0, 0, 0, None)}


def load_attempts():
    content = fetch_content()
    if content:
        pages = content['number_of_pages']
    else:
        return []
    for page in range(1, pages):
        for record in fetch_content(page)['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }


def get_midnighters():
    midnighters = []
    for attempt in load_attempts():
        if attempt['timestamp']:
            attempt_date = datetime.fromtimestamp(float(attempt['timestamp']))
            student_time = timezone(attempt['timezone']).fromutc(attempt_date).time()
            if student_time >= NIGHT_TIME['start'] and student_time < NIGHT_TIME['end']:
                attempt['time'] = str(student_time)
                midnighters.append(attempt['username'])
    return set(midnighters)


def fetch_content(page=1):
    try:
        return requests.get(URL, params={'page': page}).json()
    except requests.HTTPError as error:
        print('HTTP Error!')
        print('Response is: {0}'.format(error.response.content))
    except requests.ConnectionError:
        print('Connection failed!')
    return None


if __name__ == '__main__':
    midnighters = get_midnighters()
    if len(midnighters):
        print('Devman has midnighters:')
        for username in midnighters:
            print(username)
    else:
        print('Devman does not have midnighters')