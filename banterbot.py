from datetime import date, timedelta
from pathlib import Path
import sys

import requests

from Footy.Footy import Match

try:
    with open(Path('secret.txt'), 'r', encoding='utf-8') as secretFile:
        api_key = secretFile.read()
except:
    print('No secret.txt file found')
    sys.exit()

headers = { 'X-Auth-Token': api_key }

try:
    response = requests.get(f'https://api.football-data.org//v2/teams/64/matches/?status=FINISHED&dateFrom={date.today() - timedelta(weeks=1)}&dateTo={date.today()}', headers=headers)
except:
    print('Could not download data')
    sys.exit()

if response.status_code == requests.codes.ok:
    data = response.json()
    for matchData in data['matches']:
        match = Match(matchData)

        print()
        print(match)
else:
    print(response.content)
