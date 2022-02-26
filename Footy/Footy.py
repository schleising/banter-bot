from datetime import date
from typing import Optional

import requests

from Footy import HEADERS
from Footy.Match import Match

class Footy:
    # Set the list of teams we're interested in
    def __init__(self, teams) -> None:
        self.teams = teams

    def GetTodaysMatches(self) -> Optional[list[Match]]:
        # Initialise an empty list of matches
        matchList: list[Match] = []

        # Try to download today's matches
        try:
            response = requests.get(f'https://api.football-data.org//v2/competitions/2021/matches/?dateFrom={date.today()}&dateTo={date.today()}', headers=HEADERS)
        except:
            # In case of download failure return None to allow a retry
            print('Could not download data')
            return None

        # Check the download status is good
        if response.status_code == requests.codes.ok:
            # Deconde the JSON response
            data = response.json()

            # Set the competition name
            competiton = data['competition']['name']

            # Iterate over the matches
            for matchData in data['matches']:
                # Turn the response into a match type
                match = Match(matchData, competiton)

                # If the match involves one of the teams we're interested in append it to the match list
                if match.homeTeam in self.teams or match.awayTeam in self.teams:
                    matchList.append(match)

            # Return the match list
            return matchList

        else:
            # If the download failed, return None to allow a retry
            print(response.content)
            return None
