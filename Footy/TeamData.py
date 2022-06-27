# Map team names and stadiums
myTeamMapping = {
    'Manchester City FC': {
        'team': 'Man City',
        'ground': 'the City of Manchester Stadium',
        'name': 'Mani',
    },
}

supportedTeamMapping = {
    'Tottenham Hotspur FC': {
        'team': 'Tottenham',
        'ground': "Tottenham Hotspur Sainsbury's NFL Superstore",
        'name': 'Thommo',
    },
    'Chelsea FC': {
        'team': 'Chelsea',
        'ground': 'Stamford Bridge',
        'name': 'Tim',
    },
    'Liverpool FC': {
        'team': 'Liverpool',
        'ground': 'Anfield',
        'name': 'Stevie',
    },
}

unsupportedTeamMapping = {
    'Brighton & Hove Albion FC': {
        'team': 'Brighton',
        'ground': 'the Amex',
        'name': 'Dean',
    },
    'Arsenal FC': {
        'team': 'Arsenal',
        'ground': 'the Emirates',
        'name': '',
    },
    'Aston Villa FC': {
        'team': 'Villa',
        'ground': 'Villa Park',
        'name': '',
    },
    'Everton FC': {
        'team': 'Everton',
        'ground': 'Goodison',
        'name': '',
    },
    'Manchester United FC': {
        'team': 'Man United',
        'ground': 'Old  Trafford',
        'name': '',
    },
    'Newcastle United FC': {
        'team': 'Newcastle',
        'ground': "St James's Park",
        'name': '',
    },
    'Norwich City FC': {
        'team': 'Norwich',
        'ground': 'Carrow Road',
        'name': '',
    },
    'Wolverhampton Wanderers FC': {
        'team': 'Wolves',
        'ground': 'Molineux',
        'name': '',
    },
    'Burnley FC': {
        'team': 'Burnley',
        'ground': 'Turf Moor',
        'name': '',
    },
    'Leicester City FC': {
        'team': 'Leicester',
        'ground': 'the King Power Stadium',
        'name': '',
    },
    'Southampton FC': {
        'team': 'Southampton',
        'ground': "St Mary's",
        'name': '',
    },
    'Leeds United FC': {
        'team': 'Leeds',
        'ground': 'Elland Road',
        'name': '',
    },
    'Watford FC': {
        'team': 'Watford',
        'ground': 'Vicarage Road',
        'name': '',
    },
    'Crystal Palace FC': {
        'team': 'Palace',
        'ground': 'Selhurst Park',
        'name': '',
    },
    'Brentford FC': {
        'team': 'Brentford',
        'ground': 'the Brentford Community Stadium',
        'name': '',
    },
    'West Ham United FC': {
        'team': 'West Ham',
        'ground': 'the London Stadium',
        'name': '',
    },
    'Fulham FC': {
        'team': 'Fulham',
        'ground': 'Craven Cottage',
        'name': '',
    },
    'AFC Bournemouth': {
        'team': 'Bournemouth',
        'ground': 'Vitality Stadium',
        'name': '',
    },
    'Nottingham Forest FC': {
        'team': 'Forest',
        'ground': 'the Nottingham Forest Football Club',
        'name': '',
    },
}

teamsToWatch = myTeamMapping | supportedTeamMapping

allTeams = myTeamMapping | supportedTeamMapping | unsupportedTeamMapping

reverseTeamLookup = {val['team'].replace(' ', '').lower(): key for key, val in allTeams.items()}
