from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from zoneinfo import ZoneInfo

from pytz import timezone
from dateparser import parse

import Footy.MatchStatus as MatchStatus
from Footy.TeamData import supportedTeamMapping

@dataclass
class MatchChanges:
    firstHalfStarted: bool = False
    halfTime: bool = False
    secondHalfStarted: bool = False
    fullTime: bool = False

    teamScored: bool = False
    teamConceded: bool = False
    teamWinning: bool = False
    teamLosing: bool = False
    teamImproving: bool = False
    teamDeclining: bool = False
    teamVarFor: bool = False
    teamVarAgainst: bool = False
    teamDrawing: bool = False
    teamWon: bool = False
    teamLost: bool = False
    teamDrew: bool = False

class Match:
    def __init__(self, matchData: dict[str, Any], competition: str, oldMatch: Optional[Match] = None) -> None:
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
        self._competition = competition

        # Set the stage and group
        self._stage = matchData['stage']
        self._group = matchData['group']

        # Get the status of the match
        self.status = matchData['status']

        # Set whether my team is home or away
        if self.homeTeam in supportedTeamMapping:
            self._teamHome = True
            self._teamAway = False
        elif self.awayTeam in supportedTeamMapping:
            self._teamHome = False
            self._teamAway = True
        else:
            self._teamHome = False
            self._teamAway = False

        # Get the team name
        self.teamName = self.homeTeam if self._teamHome else self.awayTeam

        # Check whether supported teams are playing each other
        if self._teamHome and self._teamAway:
            self.supportedTeamPlayingSupportedTeam = True
        else:
            self.supportedTeamPlayingSupportedTeam = False

        # Get the match changes if the old data is available
        if oldMatch is not None:
            self.matchChanges = self._CheckStatus(oldMatch)
        else:
            self.matchChanges = MatchChanges()

    def _CheckStatus(self, oldMatch: Match) -> MatchChanges:
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

            # Check for the home team winning
            if self.homeScore > self.awayScore:
                matchChanges.teamWon = self._teamHome
                matchChanges.teamLost = self._teamAway

            # Check for the away team winning
            elif self.homeScore < self.awayScore:
                matchChanges.teamWon = self._teamAway
                matchChanges.teamLost = self._teamHome
            else:
                # Game was drawn
                if self._teamHome or self._teamAway:
                    matchChanges.teamDrew = True

        # Check for a home goal
        if oldMatch.homeScore < self.homeScore:
            matchChanges.teamScored = self._teamHome
            matchChanges.teamConceded = self._teamAway

            # If the home team scored, but they're still behind or drawing then they're improving
            if self.homeScore <= self.awayScore:
                matchChanges.teamImproving = self._teamHome
                matchChanges.teamDeclining = self._teamAway

        # Check for home VAR goal reversal
        elif oldMatch.homeScore > self.homeScore:
            matchChanges.teamVarAgainst = self._teamHome
            matchChanges.teamVarFor = self._teamAway

        # Check for an away goal
        if oldMatch.awayScore < self.awayScore:
            matchChanges.teamScored = self._teamAway
            matchChanges.teamConceded = self._teamHome

            # If the away team scored, but they're still behind or drawing then they're improving
            if self.awayScore <= self.homeScore:
                matchChanges.teamImproving = self._teamAway
                matchChanges.teamDeclining = self._teamHome

        # Check for home VAR goal reversal
        elif oldMatch.awayScore > self.awayScore:
            matchChanges.teamVarAgainst = self._teamAway
            matchChanges.teamVarFor = self._teamHome

        # Check for the home team winning
        if self.homeScore > self.awayScore:
            matchChanges.teamWinning = self._teamHome
            matchChanges.teamLosing = self._teamAway

        # Check for the away team winning
        elif self.awayScore > self.homeScore:
            matchChanges.teamWinning = self._teamAway
            matchChanges.teamLosing = self._teamHome
        else:
            # Game is being drawn
            if self._teamHome or self._teamAway:
                matchChanges.teamDrawing = True

        # Return the changes
        return matchChanges

    # Convert this match into a string for printing
    def __str__(self) -> str:
        # Create a string for the match details
        matchDetails = f'{self.matchDate.astimezone(tz=ZoneInfo("Europe/London")).strftime("%c %Z")} - {self._competition} - Stage: {self._stage} - Group: {self._group}'

        # Create a string for the scoreline
        scoreLine = f'{self.homeTeam} {self.homeScore} - {self.awayScore} {self.awayTeam} - {self.status}'

        # Return the two strings separated by a new line
        return f'{matchDetails}\n{scoreLine}'
