from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from pytz import timezone
from dateparser import parse

import Footy.MatchStatus as MatchStatus

@dataclass
class MatchChanges:
    firstHalfStarted: bool = False
    halfTime: bool = False
    secondHalfStarted: bool = False
    fullTime: bool = False

    homeTeamScored: bool = False
    awayTeamScored: bool = False

    homeTeamWinning: bool = False
    awayTeamWinning: bool = False

    homeTeamImproving: bool = False
    awayTeamImproving: bool = False

class Match:
    def __init__(self, matchData: dict[str, Any], competition: str) -> None:
        # Get the match ID
        self.id = matchData['id']

        # Get the home and away team names
        self.homeTeam = matchData['homeTeam']['name']
        self.awayTeam = matchData['awayTeam']['name']

        # Get the full time score, replacing None with TBD
        self.homeScore = matchData['score']['fullTime']['homeTeam'] if matchData['score']['fullTime']['homeTeam'] is not None else 'TBD'
        self.awayScore = matchData['score']['fullTime']['awayTeam'] if matchData['score']['fullTime']['awayTeam'] is not None else 'TBD'

        # Get and parse the match date and time, times are all UTC, so make sure the datetime is aware
        matchDate = parse(matchData['utcDate'])
        if matchDate is None:
            self.matchDate = datetime(1900, 1, 1).replace(tzinfo=timezone('UTC'))
        else:
            self.matchDate = matchDate.replace(tzinfo=timezone('UTC'))

        # Set the competition name
        self.competition = competition

        # Set the stage and group
        self.stage = matchData['stage']
        self.group = matchData['group']

        # Get the status of the match
        self.status = matchData['status']

    def CheckStatus(self, oldMatch: Match) -> MatchChanges:
        # Check for various state changes in the match
        matchChanges = MatchChanges()

        # Check whether the match has started
        if oldMatch.status == MatchStatus.scheduled and self.status == MatchStatus.inPlay:
            matchChanges.firstHalfStarted = True

        # Check for half time
        elif oldMatch.status == MatchStatus.inPlay and self.status == MatchStatus.paused:
            matchChanges.halfTime = True

        # Check for the start of the second half
        elif oldMatch.status == MatchStatus.paused and self.status == MatchStatus.inPlay:
            matchChanges.secondHalfStarted = True

        # Check for full time
        elif oldMatch.status == MatchStatus.inPlay and self.status == MatchStatus.finished:
            matchChanges.fullTime = True

        # Check for a home goal
        if oldMatch.homeScore < self.homeScore:
            matchChanges.homeTeamScored = True

            # If the home team scored, but they're still behind or drawing then they're improving
            if self.homeScore <= self.awayScore:
                matchChanges.homeTeamImproving = True

        # Check for an away goal
        if oldMatch.awayScore < self.awayScore:
            matchChanges.awayTeamScored = True

            # If the away team scored, but they're still behind or drawing then they're improving
            if self.awayScore <= self.homeScore:
                matchChanges.awayTeamImproving = True

        # Check for the home team winning
        if self.homeScore > self.awayScore:
            matchChanges.homeTeamWinning = True

        # Check for the away team winning
        elif self.awayScore > self.homeScore:
            matchChanges.awayTeamWinning = True

        # Return the changes
        return matchChanges


    # Convert this match into a string for printing
    def __str__(self) -> str:
        # Create a string for the match details
        matchDetails = f'{self.matchDate.astimezone(tz=ZoneInfo("Europe/London")).strftime("%c %Z")} - {self.competition} - Stage: {self.stage} - Group: {self.group}'

        # Create a string for the scoreline
        scoreLine = f'{self.homeTeam} {self.homeScore} - {self.awayScore} {self.awayTeam} - {self.status}'

        # Return the two strings separated by a new line
        return f'{matchDetails}\n{scoreLine}'
