from datetime import datetime
import json

def calculate(date: datetime, mutetime):
    hour = date.hour
    mutesec = round(date.second) + mutetime
    mutemin = date.minute
    if mutesec == 60:
        mutesec = 0
        mutemin += 1
    elif mutesec > 60:
        print(mutesec, mutemin)
        mutemin += (mutesec // 60)
        while mutesec >= 60:
            mutesec -= 60
    if mutemin == 60:
        mutemin = 0
        hour += 1
    elif mutemin > 60:
        print(mutemin, hour)
        hour += (mutesec // 60)
        while mutesec >= 60:
            mutesec -= 60
    muted_date = datetime(date.year, date.month, date.day, hour, mutemin, mutesec)
    return muted_date