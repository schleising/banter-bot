from dataclasses import dataclass
from typing import Any, Dict
import requests

from Footy import HEADERS

# Class containing a single entry in the table
@dataclass
class TableEntry:
    Position: int
    TeamName: str
    Played: int
    Won: int
    Drawn: int
    Lost: int
    Points: int
    GoalsFor: int
    GoalsAgainst: int
    GoalDifference: int

    # Format the entry for printing in a table
    def __str__(self) -> str:
        return f'{self.Position:<6}{self.TeamName:28}{self.Played:8}{self.Won:6}{self.Drawn:8}{self.Lost:6}{self.GoalsFor:6}{self.GoalsAgainst:8}{self.GoalDifference:6}{self.Points:8}'

# Class for the full table
class Table:
    def __init__(self) -> None:
        # Initialise member variables to safe defaults
        self.Competition: str = 'Error, no competition set'
        self.Entries: Dict[str, TableEntry] = {}
        self.MaxGames = 0
        self.PointsForWin = 3
        self.PointsForDraw = 1

        # Get the table data
        try:
            response = requests.get('http://api.football-data.org/v2/competitions/2021/standings', headers=HEADERS)
        except:
            # Return in the event of a failure
            print('Could not download table data')
            return

        if response.status_code == requests.codes.ok:
            # If the response is OK (200), parse the table data into entries
            data = response.json()
            self._ParseTable(data)
        else:
            # Return in the event of a failure
            print(response.content)
            return

    def _ParseTable(self, data: Dict[str, Any]):
        self.Competition = data['competition']['name']

        for entry in data['standings'][0]['table']:
            position = int(entry['position'])
            teamName = str(entry['team']['name'])
            played = int(entry['playedGames'])
            won = int(entry['won'])
            drawn = int(entry['draw'])
            lost = int(entry['lost'])
            points = int(entry['points'])
            goalsFor = int(entry ['goalsFor'])
            goalsAgainst = int(entry['goalsAgainst'])
            goalDifference = int(entry['goalDifference'])

            tableEntry = TableEntry(
                position,
                teamName,
                played,
                won,
                drawn,
                lost,
                points,
                goalsFor,
                goalsAgainst,
                goalDifference
                )

            self.Entries[teamName] = tableEntry

        self.MaxGames = 2 * (len(self.Entries) - 1)

    def CanTeamABeatTeamB(self, teamA: str, teamB: str) -> bool:
        # Check both teams are in the table
        if teamA in self.Entries and teamB in self.Entries:
            # If so get their respective entries
            teamAEntry = self.Entries[teamA]
            teamBEntry = self.Entries[teamB]

            # Work out how many points team A can get if they win all remaining games
            teamAMaxPoints = teamAEntry.Points + (self.PointsForWin * (self.MaxGames - teamAEntry.Played))

            # If this is greater than or equal to the current number of points team B has, then team A can still beat team B
            if teamAMaxPoints >= teamBEntry.Points:
                return True
            else:
                return False
        else:
            return False

    def CanTeamWinTheLeague(self, team: str) -> bool:
        # Get a copy of the entries
        teamList = dict(self.Entries)

        # Remove the current team from the copy of the entries
        teamList.pop(team)

        # If team can still beat all other teams then it can win the league
        if all(self.CanTeamABeatTeamB(team, otherTeam) for otherTeam in teamList):
            return True
        else:
            return False

    def __str__(self) -> str:
        if self.Entries:
            tableHeader = f'{"Pos":6}{"Team":28}{"Played":>8}{"Won":>6}{"Drawn":>8}{"Lost":>6}{"For":>6}{"Against":>8}{"GD":>6}{"Points":>8}\n'
            tableEntries = '\n'.join(str(entry) for entry in self.Entries.values())
            return f'{self.Competition} Table\n{tableHeader}\n{tableEntries}'
        else:
            return 'Error, cannot print table, no data downloaded'
