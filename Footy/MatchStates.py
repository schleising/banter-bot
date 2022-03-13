from __future__ import annotations
from typing import Optional

class MatchState:
    def __init__(self, teamScore: int = 0, oppositionScore: int = 0) -> None:
        self.teamScore = teamScore
        self.oppositionScore = oppositionScore
        self.oldScoreDifference = self.teamScore - self.oppositionScore

    def FindState(self) -> Optional[MatchState]:
        scoreDifference = self.teamScore - self.oppositionScore

        match scoreDifference:
            case 1:
                returnVal = TeamLeadByOne(self.teamScore, self.oppositionScore)
            case -1:
                returnVal = TeamDeficitOfOne(self.teamScore, self.oppositionScore)
            case x if x > 1:
                returnVal = TeamExtendingLead(self.teamScore, self.oppositionScore)
            case x if x < -1:
                returnVal = TeamExtendingDeficit(self.teamScore, self.oppositionScore)
            case _:
                returnVal = Drawing(self.teamScore, self.oppositionScore)

        return returnVal

    def __str__(self) -> str:
        return f'State: {self.__class__.__name__:20} Team Score {self.teamScore} - {self.oppositionScore} Opposition Score'

class Drawing(MatchState):
    def GoalScored(self, teamScore: int, oppositionScore: int) -> Optional[MatchState]:
        scoreDifference = teamScore - oppositionScore

        match scoreDifference:
            case 1:
                returnVal = TeamLeadByOne(teamScore, oppositionScore)
            case -1:
                returnVal = TeamDeficitOfOne(teamScore, oppositionScore)
            case _:
                print(f'Attempted to move from {__class__.__name__} to invalid state {teamScore} - {oppositionScore}')
                returnVal = MatchState(teamScore, oppositionScore).FindState()

        return returnVal

class TeamLeadByOne(MatchState):
    def GoalScored(self, teamScore: int, oppositionScore: int) -> Optional[MatchState]:
        scoreDifference = teamScore - oppositionScore

        match scoreDifference:
            case 0:
                returnVal = Drawing(teamScore, oppositionScore)
            case scoreDifference if scoreDifference > 1:
                returnVal = TeamExtendingLead(teamScore, oppositionScore)
            case _:
                print(f'Attempted to move from {__class__.__name__} to invalid state {teamScore} - {oppositionScore}')
                returnVal = MatchState(teamScore, oppositionScore).FindState()

        return returnVal

class TeamExtendingLead(MatchState):
    def GoalScored(self, teamScore: int, oppositionScore: int) -> Optional[MatchState]:
        scoreDifference = teamScore - oppositionScore
        scoreDirection = scoreDifference - self.oldScoreDifference

        match scoreDifference, scoreDirection:
            case 1, _:
                returnVal = TeamLeadByOne(teamScore, oppositionScore)
            case _, scoreDirection if scoreDirection < 0:
                returnVal = TeamLosingLead(teamScore, oppositionScore)
            case _, scoreDirection if scoreDirection > 0:
                returnVal = TeamExtendingLead(teamScore, oppositionScore)
            case _:
                print(f'Attempted to move from {__class__.__name__} to invalid state {teamScore} - {oppositionScore}')
                returnVal = MatchState(teamScore, oppositionScore).FindState()

        return returnVal

class TeamLosingLead(MatchState):
    def GoalScored(self, teamScore: int, oppositionScore: int) -> Optional[MatchState]:
        scoreDifference = teamScore - oppositionScore
        scoreDirection = scoreDifference - self.oldScoreDifference

        match scoreDifference, scoreDirection:
            case 1, _:
                returnVal = TeamLeadByOne(teamScore, oppositionScore)
            case _, scoreDirection if scoreDirection < 0:
                returnVal = TeamLosingLead(teamScore, oppositionScore)
            case _, scoreDirection if scoreDirection > 0:
                returnVal = TeamExtendingLead(teamScore, oppositionScore)
            case _:
                print(f'Attempted to move from {__class__.__name__} to invalid state {teamScore} - {oppositionScore}')
                returnVal = MatchState(teamScore, oppositionScore).FindState()

        return returnVal

class TeamDeficitOfOne(MatchState):
    def GoalScored(self, teamScore: int, oppositionScore: int) -> Optional[MatchState]:
        scoreDifference = teamScore - oppositionScore

        match scoreDifference:
            case 0:
                returnVal = Drawing(teamScore, oppositionScore)
            case scoreDifference if scoreDifference < -1:
                returnVal = TeamExtendingDeficit(teamScore, oppositionScore)
            case _:
                print(f'Attempted to move from {__class__.__name__} to invalid state {teamScore} - {oppositionScore}')
                returnVal = MatchState(teamScore, oppositionScore).FindState()

        return returnVal

class TeamExtendingDeficit(MatchState):
    def GoalScored(self, teamScore: int, oppositionScore: int) -> Optional[MatchState]:
        scoreDifference = teamScore - oppositionScore
        scoreDirection = scoreDifference - self.oldScoreDifference

        match scoreDifference, scoreDirection:
            case -1, _:
                returnVal = TeamDeficitOfOne(teamScore, oppositionScore)
            case _, scoreDirection if scoreDirection < 0:
                returnVal = TeamExtendingDeficit(teamScore, oppositionScore)
            case _, scoreDirection if scoreDirection > 0:
                returnVal = TeamLosingDeficit(teamScore, oppositionScore)
            case _:
                print(f'Attempted to move from {__class__.__name__} to invalid state {teamScore} - {oppositionScore}')
                returnVal = MatchState(teamScore, oppositionScore).FindState()

        return returnVal

class TeamLosingDeficit(MatchState):
    def GoalScored(self, teamScore: int, oppositionScore: int) -> Optional[MatchState]:
        scoreDifference = teamScore - oppositionScore
        scoreDirection = scoreDifference - self.oldScoreDifference

        match scoreDifference, scoreDirection:
            case -1, _:
                returnVal = TeamDeficitOfOne(teamScore, oppositionScore)
            case _, scoreDirection if scoreDirection < 0:
                returnVal = TeamExtendingDeficit(teamScore, oppositionScore)
            case _, scoreDirection if scoreDirection > 0:
                returnVal = TeamLosingDeficit(teamScore, oppositionScore)
            case _:
                print(f'Attempted to move from {__class__.__name__} to invalid state {teamScore} - {oppositionScore}')
                returnVal = MatchState(teamScore, oppositionScore).FindState()

        return returnVal
