from Footy.Table import Table

table = Table()
print(table)

for entry in table.Entries:
    print(f'Can {entry} beat Liverpool?  {"Yes" if table.CanTeamABeatTeamB(entry, "Liverpool FC") else "No"}')
