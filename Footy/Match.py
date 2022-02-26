from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from dateparser import parse

class Match:
    def __init__(self, matchData: dict[str, Any], competition: str) -> None:
        # Get the home and away team names
        self.homeTeam = matchData['homeTeam']['name']
        self.awayTeam = matchData['awayTeam']['name']

        # Get the full time score, replacing None with TBD
        self.homeScore = matchData['score']['fullTime']['homeTeam'] if matchData['score']['fullTime']['homeTeam'] is not None else 'TBD'
        self.awayScore = matchData['score']['fullTime']['awayTeam'] if matchData['score']['fullTime']['awayTeam'] is not None else 'TBD'

        # Get and parse the match date and time, times are all UTC, so make sure the datetime is aware
        matchDate = parse(matchData['utcDate'])
        if matchDate is None:
            self.matchDate = datetime(1900, 1, 1)
        else:
            self.matchDate = matchDate

        # Set the competition name
        self.competition = competition

        # Set the stage and group
        self.stage = matchData['stage']
        self.group = matchData['group']

    # Convert this match into a string for printing
    def __str__(self) -> str:
        # Create a string for the match details
        matchDetails = f'{self.matchDate.astimezone(tz=ZoneInfo("Europe/London")).strftime("%c %Z")} - {self.competition} - Stage: {self.stage} - Group: {self.group}'

        # Create a string for the scoreline
        scoreLine = f'{self.homeTeam} {self.homeScore} - {self.awayScore} {self.awayTeam}'

        # Return the two strings separated by a new line
        return f'{matchDetails}\n{scoreLine}'
