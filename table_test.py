from Footy.Table import Table

table = Table()
print(table)

print()

for entry in table.Entries:
    print(f'Can {entry} beat Liverpool?  {"Yes" if table.CanTeamABeatTeamB(entry, "Liverpool FC") else "No"}')

print()

for entry in table.Entries:
    print(f'Can {entry} win the league?  {"Yes" if table.CanTeamWinTheLeague(entry) else "No"}')
