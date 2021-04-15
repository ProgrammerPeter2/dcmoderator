from datetime import datetime
import csv_manager
import modifier

def getMuteData(user):
    usermutes = open("datas/mutes.txt", "r", encoding="utf8").read().split(";")
    _usermutes = list()
    for u in usermutes:
        usermutes.remove(u)
        print(type(u))
        lista = u.split(",")
        _usermutes.append(lista)
    index = 0
    for i in range(len(_usermutes)):
        if _usermutes[i][0] == user:
            index = i
    return _usermutes, index

def calculate(user, date, mutetime):
    hour = date.hour
    mutesec = round(date.second) + mutetime
    mutemin = date.minute
    print(mutemin, type(mutemin))
    if mutesec == 60:
        mutesec = 0
        mutemin += 1
    elif mutesec > 60:
        mutemin = (mutesec // 60)
        mutesec = mutesec - (mutemin * 60)
    print(mutemin)
    muted_date = datetime(date.year, date.month, date.day, hour, mutemin, mutesec)
    mute, index = getMuteData(user)
    print(mute[index])