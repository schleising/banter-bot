# Map team names and stadiums
# myTeamMapping = {
# }

supportedTeamMapping = {
    'Tottenham Hotspur FC': {
        'name': 'Tottenham',
        'ground': "Tottenham Hotspur Sainsbury's NFL Superstore",
    },
    'Chelsea FC': {
        'name': 'Chelsea',
        'ground': 'Stamford Bridge',
    },
    'Liverpool FC': {
        'name': 'Liverpool',
        'ground': 'Anfield',
    },
    'Manchester City FC': {
        'name': 'Man City',
        'ground': 'the City of Manchester Stadium',
    },
    'Arsenal FC': {
        'name': 'Arsenal',
        'ground': 'the Emirates',
    },
}

unsupportedTeamMapping = {
    'Aston Villa FC': {
        'name': 'Villa',
        'ground': 'Villa Park',
    },
    'Everton FC': {
        'name': 'Everton',
        'ground': 'Goodison',
    },
    'Manchester United FC': {
        'name': 'Man United',
        'ground': 'Old  Trafford',
    },
    'Newcastle United FC': {
        'name': 'Newcastle',
        'ground': "St James's Park",
    },
    'Norwich City FC': {
        'name': 'Norwich',
        'ground': 'Carrow Road',
    },
    'Wolverhampton Wanderers FC': {
        'name': 'Wolves',
        'ground': 'Molineux',
    },
    'Burnley FC': {
        'name': 'Burnley',
        'ground': 'Turf Moor',
    },
    'Leicester City FC': {
        'name': 'Leicester',
        'ground': 'the King Power Stadium',
    },
    'Southampton FC': {
        'name': 'Southampton',
        'ground': "St Mary's",
    },
    'Leeds United FC': {
        'name': 'Leeds',
        'ground': 'Elland Road',
    },
    'Watford FC': {
        'name': 'Watford',
        'ground': 'Vicarage Road',
    },
    'Crystal Palace FC': {
        'name': 'Palace',
        'ground': 'Selhurst Park',
    },
    'Brighton & Hove Albion FC': {
        'name': 'Brighton',
        'ground': 'the Amex',
    },
    'Brentford FC': {
        'name': 'Brentford',
        'ground': 'the Brentford Community Stadium',
    },
    'West Ham United FC': {
        'name': 'West Ham',
        'ground': 'the London Stadium',
    },
}

# teamsToWatch = myTeamMapping | supportedTeamMapping
teamsToWatch = supportedTeamMapping

# allTeams = myTeamMapping | supportedTeamMapping | unsupportedTeamMapping
allTeams = supportedTeamMapping | unsupportedTeamMapping
