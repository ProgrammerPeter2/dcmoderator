def makeLogs(logs: list):
    logData = []
    for log in logs:
        _id = log[0]
        user = log[1]
        target = log[2]
        deadline = log[3]
        date = ""
        action = log[4]
        logText = ""
        if action == "mute":
            logText = f"{user.capitalize()} némította {target} felhasználót eddig: {deadline}."
        elif action == "unmute":
            logText = f"{user.capitalize()} feloldotta {target} felhasználó némítását."
            date = deadline
        elif action == "getmute":
            logText = f"{user.capitalize()} lekérte az összes aktív némítást."
            date = deadline
        elif action == "gbw":
            logText = f"{user.capitalize()} listáztatta az összes tiltott szót."
            date = deadline
        elif action == "cls":
            date = deadline
            logText = f"{user.capitalize()} sikeresen kitörölt {action[4:]} üzenetet a(z) {target} csatornáról"
        elif action == "clf":
            date = deadline
            ok = ""
            if action[4:] == "mr":
                ok = "nem volt jogultsága hozzá!"
            logText = f"{user.capitalize()} megpróbált kitörölni pár üzenetet a(z) {target} csatornáról, de {ok}"
        elif action == "lis":
            date = deadline
            logText = f"{user.capitalize()} bejelentkezett az online kezelőfelületbe."
        elif action == "lif":
            date = deadline
            logText = f"A(z) {user.capitalize()} ip címről valaki megpróbált bejelentkezni az online kezelőfelületre."
        elif action == "lo":
            date = deadline
            logText = f"{user.capitalize()} kijelentkezett az online kezelőfelületről."
        elif action == "dbw":
            date = deadline
            logText = f"{user.capitalize()} törölte a(z) {target.lower()} a tiltott szavak listájából."
        elif action == "abw":
            date = deadline
            logText = f"{user.capitalize()} hozzáadta a következő szót a tiltott szavak listájához: {target.lower()}."
        elif action == "rnc":
            date = deadline
            logText = f"{user.capitalize()} nullázta a némítás számlálót."
        elif action == "mdu":
            date = deadline
            logText = f"{user.capitalize()} módosította {target.capitalize()} felhasználó adatait."
        elif action == "cu":
            date = deadline
            logText = f"{user.capitalize()} létrehozta {target.capitalize()} felhasználót."
        elif action == "du":
            date = deadline
            logText = f"{user.capitalize()} törölte {target.capitalize()} felhasználót."
        elif action == "dl":
            date = deadline
            logText = f"{user.capitalize()} törölte az összes logot!"
        logData.append([_id, date, logText])
    return logData

def rankDecoder(rank: int):
    _return = ""
    if rank == 1:
        _return = "Moderátor"
    elif rank == 5:
        _return = "Globális adminisztrátor"
    return _return

def rankEncoder(rank: str):
    rankid = 0
    if rank.lower() == "moderátor":
        rankid = 1
    elif rank.lower() == "globális adminisztrátor":
        rankid = 5
    return rankid
