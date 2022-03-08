from datetime import date
from typing import Optional

import requests

from Footy import HEADERS
from Footy.Match import Match
import Footy.MatchStatus as MatchStatus

class Footy:
    # Set the list of teams we're interested in
    def __init__(self, teams: Optional[list[str]] = None) -> None:
        # If a team list is given, use that
        if teams is not None:
            self.teams = teams
        else:
            # If no team list is given, download the full list of Proemier League teams
            try:
                response = requests.get(f'https://api.football-data.org/v2/competitions/2021/teams', headers=HEADERS)
            except:
                # In case of download failure return None to allow a retry
                print('Could not download data')
                return

            # Check the download status is good
            if response.status_code == requests.codes.ok:
                # Add the teams to the list
                data = response.json()
                self.teams = [team['name'] for team in data['teams']]
            else:
                # If the download failed, return None to allow a retry
                print(response.content)
                return

    def GetMatches(self, dateFrom: Optional[date] = None, dateTo: Optional[date] = None) -> Optional[list[Match]]:
        # Initialise an empty list of matches
        matchList: list[Match] = []

        # Sort out the dates
        if dateFrom is None:
            dateFrom = date.today()
        if dateTo is None or dateTo < dateFrom:
            dateTo = dateFrom

        # Try to download today's matches
        try:
            response = requests.get(f'https://api.football-data.org//v2/competitions/2021/matches/?dateFrom={dateFrom}&dateTo={dateTo}', headers=HEADERS)
        except:
            # In case of download failure return None to allow a retry
            print('Could not download data')
            return None

        # Check the download status is good
        if response.status_code == requests.codes.ok:
            # Decode the JSON response
            data = response.json()

            # Set the competition name
            competiton = data['competition']['name']

            # Iterate over the matches
            for matchData in data['matches']:
                # Turn the response into a match type
                match = Match(matchData, competiton)

                # If the match involves one of the teams we're interested in append it to the match list
                if match.homeTeam in self.teams or match.awayTeam in self.teams:
                    # Check that the match may be on today
                    if match.status in MatchStatus.matchToBePlayedList:
                        matchList.append(match)

            # Return the match list
            return matchList

        else:
            # If the download failed, return None to allow a retry
            print(response.content)
            return None

    def GetMatch(self, oldMatch: Match) -> Optional[Match]:
        # Try to download today's matches
        try:
            response = requests.get(f'https://api.football-data.org//v2/matches/{oldMatch.id}', headers=HEADERS)
        except:
            # In case of download failure return None to allow a retry
            print('Could not download data')
            return None

        # Check the download status is good
        if response.status_code == requests.codes.ok:
            # Decode the JSON response
            data = response.json()

            # Get the competition
            competition = data['match']['competition']['name']

            # Create and return a match from the data
            return Match(data['match'], competition, oldMatch)
        else:
            # If the download failed, return None to allow a retry
            print(response.content)
            return None
