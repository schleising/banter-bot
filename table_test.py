from Footy.Table import Table

table = Table()
print(table)

print()

for team in table.Entries:
    print(f'Can {team} beat Liverpool FC?  {"Yes" if table.CanTeamABeatTeamB(team, "Liverpool FC") else "No"}')

print()

for team in table.Entries:
    print(f'Can {team} win the league?  {"Yes" if table.CanTeamWinTheLeague(team) else "No"}')

print()

for team in table.Entries:
    print(f'Have {team} won the league?  {"Yes" if table.HasTeamWonTheLeague(team) else "No"}')

print()

teamWonLeague = table.HasAnyTeamWonTheLeague()
print(f'{teamWonLeague + " have" if teamWonLeague is not None else "No team has"} won the league')
