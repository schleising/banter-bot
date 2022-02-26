from Footy.Footy import Footy

# Set the teams we're interested in
teams = [
    'Liverpool FC',
    'Chelsea FC',
    'Tottenham Hotspur FC',
]

# Create a Footy object using the list of teams we're interested in
footy = Footy(teams)

# Get today's matches for the teams in the list
todaysMatches = footy.GetTodaysMatches()

# If the download was successful, print the matches
if todaysMatches is not None:
    for match in todaysMatches:
        print()
        print(match)
else:
    print('Download Failed')
