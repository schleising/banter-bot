from datetime import date, timedelta
from Footy.Footy import Footy

footy = Footy()

matches = footy.GetMatches(date.today() + timedelta(days=1))

if matches is not None:
    for match in matches:
        print(match)
