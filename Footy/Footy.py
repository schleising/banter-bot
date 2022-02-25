from datetime import datetime
from typing import Any

from dateparser import parse

class Match:
    def __init__(self, matchData: dict[str, Any]) -> None:
        self.homeTeam = matchData['homeTeam']['name']
        self.awayTeam = matchData['awayTeam']['name']
        self.homeScore = matchData['score']['fullTime']['homeTeam'] if matchData['score']['fullTime']['homeTeam'] is not None else 'TBD'
        self.awayScore = matchData['score']['fullTime']['awayTeam'] if matchData['score']['fullTime']['awayTeam'] is not None else 'TBD'
        matchDate = parse(matchData['utcDate'], settings={'TIMEZONE': 'UTC'})
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
