from datetime import datetime
from pathlib import Path
import sys
from typing import Any
import requests

from dateparser import parse

class Match:
    def __init__(self, matchData: dict[str, Any]) -> None:
        self.homeTeam = matchData['homeTeam']['name']
        self.awayTeam = matchData['awayTeam']['name']
        self.homeScore = matchData['score']['fullTime']['homeTeam'] if matchData['score']['fullTime']['homeTeam'] is not None else "TBD"
        self.awayScore = matchData['score']['fullTime']['awayTeam'] if matchData['score']['fullTime']['awayTeam'] is not None else "TBD"
        matchDate = parse(matchData['utcDate'])
        if matchDate is None:
            self.matchDate = datetime(1900, 1, 1)
        else:
            self.matchDate = matchDate
        self.competition = matchData['competition']['name']
        self.stage = matchData['stage']
        self.group = matchData['group']

    def __str__(self) -> str:
        matchDetails = f'{self.matchDate.date()} - {self.competition} - Stage: {self.stage} - Group: {self.group}'
        scoreLine = f'{self.homeTeam} {self.homeScore} - {self.awayScore} {self.awayTeam}'

        return f'{matchDetails}\n{scoreLine}'

try:
    with open(Path('secret.txt'), 'r', encoding='utf-8') as secretFile:
        api_key = secretFile.read()
except:
    print('No secret.txt file found')
    sys.exit()

headers = { 'X-Auth-Token': api_key }

response = requests.get('http://api.football-data.org//v2/teams/64/matches/', headers=headers)

if response.status_code == requests.codes.ok:
    data = response.json()
    for matchData in data['matches']:
        match = Match(matchData)

        print()
        print(match)
else:
    print(response.content)
