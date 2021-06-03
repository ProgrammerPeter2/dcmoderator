from flask import *
import db_manage
import logMaker as log
from libs import modifier
import discord_webhook as webhook

app = Flask(__name__)
app.secret_key = '1234'

@app.route('/')
def index():
    msg = ""
    err = ""
    if session.get("error", None) is not None:
        err = session.get("error", None)
        session["error"] = ""
    if session.get("msg", None) is not None:
        msg = session.get("msg", None)
        session["msg"] = ""
    return render_template("index.html", error=err, message=msg)


@app.route('/login', methods=['post'])
def login():
    uname = request.form.get('uname')
    passw = request.form.get('pass')
    session['rank'] = 0
    user_datas = db_manage.select("users", ["*"], "")
    ip = request.environ['REMOTE_ADDR']
    loggedIn = False
    username = ""
    rank: int
    if len(user_datas) == 0:
        for user in user_datas:
            if user[1] == uname and user[2] == passw:
                loggedIn = True
                username = user[3]
                rank = user[5]
        if loggedIn:
            session['name'] = username
            session['rank'] = rank
            db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                             f"0, '{username}', '', '{modifier.date_string()}', 'lis'")
            return redirect(location='/home')
        else:
            db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                             f"0, '{ip}', '', '', 'lif'")
            session['error'] = "Something went wrong with your login datas!"
            return redirect(location="/")
    else:
        session['error'] = "Sorry we are lost connection with mysql server! Please try again later!"
        return redirect(location='/')

@app.route('/home')
def home():
    if session.get('rank', 0) > 0:
        datas = db_manage.select("mutes", ["*"], "")
        mutes = []
        if len(datas) > 0:
            for data in datas:
                _id = data[0]
                uname = data[3]
                mutedate = data[2]
                mutes.append([_id, uname, mutedate])
        else:
            mutes.append(["", "Nincs egy aktív némítás sem!", ""])
        session["order"] = "normal"
        logs = db_manage.select("logs", ["*"], "ORDER BY id DESC LIMIT 15")
        logData = log.makeLogs(logs)
        badWords = db_manage.select("badwords", ["*"], "")
        badwords = []
        userLink = ""
        userText = ""
        if session.get("rank", None) == 5:
            userText = "Felhasználókezelés"
            userLink = "/home/userManager/"
        for word in badWords:
            badwords.append(modifier.rem_char(word))
        return render_template("home.html", user=session.get('name', None), datas=mutes,
                               logs=logData, words=badwords, usertext=userText, userlink=userLink)
    else:
        session['error'] = "You are not logged in! Please login or ask moderators for permission!"
        return redirect('/')

@app.route('/rc')
def reset_mute_counter():
    db_manage.execute("ALTER TABLE mutes AUTO_INCREMENT = 1")
    db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                     f"0, '{session.get('name', None)}', '', '{modifier.date_string()}', 'rnc'")
    return redirect('/home')

@app.route('/home/logs')
def logs():
    extra = ""
    if session.get('order', None) == "normal":
        extra = "ORDER BY id DESC"
    logs = db_manage.select("logs", ["*"], extra)
    logData = log.makeLogs(logs)
    link = ""
    text = ""
    if session.get('rank', None) == 5:
        link = "/home/logs/truncate"
        text = "Logok törlése"
    return render_template("logs.html", logs=logData, truncateLink=link, truncateText=text)

@app.route('/home/logs/order', methods=["post"])
def logs_action():
    order = request.form.get('order')
    if order == "Régebbiek elől":
        session['order'] = ""
    elif order == "Nem túl régi esmények elől":
        session['order'] = "normal"
    return redirect('/home/logs')

@app.route('/home/logs/truncate')
def logs_delete():
    db_manage.execute("TRUNCATE logs")
    db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                     f"0, '{session.get('name', None)}', '', '{modifier.date_string()}', 'dl'")
    return redirect('/home')

@app.route('/bwa')
def bad_words_action():
    action = request.args.get('act')
    _redirect = '/home'
    if action == "new":
        _redirect = '/home/new_badWord'
    elif action == "del":
        word = request.args.get('word')
        text = f"{session.get('name', None).capitalize()} törölte a(z) {word} szót a tiltott szavak listájából"
        webhook.sendWebhook(text)
        db_manage.remove("badwords", f"badword='{word}'")
        db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                         f"0, '{session.get('name', None)}', '{word}', '{modifier.date_string()}', 'dbw'")
    return redirect(_redirect)

@app.route('/home/new_badWord')
def new_bad_word():
    err = ""
    if session.get("bwerr", None) is not None:
        err = session.get("bwerr", None)
        session["bwerr"] = ""
    return render_template("bwc.html", error=err)

@app.route('/bwadd', methods=['post'])
def addBadWord():
    word = request.form.get('word')
    _redirect = '/home'
    badWords = db_manage.select("badwords", ["*"], "")
    if not word in badWords:
        text = f"{session.get('name', None).capitalize()} hozzáadta a {word} szót a tiltott szavak listájához!"
        webhook.sendWebhook(text, "Tiltott szó hozzáadása")
        db_manage.insert("badwords", ['badword'], f"'{word}'")
        db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                         f"0, '{session.get('name', None)}', '{word}', '{modifier.date_string()}', 'abw'")
    else:
        session["bwerr"] = "A szó már szerepel a listában. Kérlek adj meg egy másik szót!"
        _redirect = '/home/new_badWord'
    return redirect('/home')

@app.route('/home/userManager/')
def userManager():
    _users = db_manage.select("users", ["*"], "")
    users = []
    msg = ""
    err = ""
    if session.get("uer", None) is not None:
        err = session.get("uer", None)
        session["uer"] = ""
    if session.get("umsg", None) is not None:
        msg = session.get("uemsg", None)
        session["uemsg"] = ""
    for user in _users:
        _id = user[0]
        uname = user[1]
        dcname = user[4]
        name = user[3]
        rank = log.rankDecoder(int(user[5]))
        users.append([_id, uname, name, dcname, rank])
    return render_template("user_manager.html", users=users, msg=msg, error=err)

@app.route('/home/userManager/modifyuser')
def modifySite():
    modifyUser = db_manage.select("users", ["*"], f"WHERE ud={request.args.get('uid')}")[0]
    _id = modifyUser[0]
    session["muid"] = _id
    uname = modifyUser[1]
    name = modifyUser[3]
    dcname = modifyUser[4]
    rank = log.rankDecoder(int(modifyUser[5]))
    _ranks = ["Moderátor", "Globális adminisztátor"]
    ranks = []
    for Rank in _ranks:
        outlist = [Rank]
        if Rank == rank:
            outlist.append("selected")
        else:
            outlist.append("")
        ranks.append(outlist)
    return render_template("user_modifier.html", userDatas=[_id, uname, name, dcname, rank], ranks=ranks)

@app.route('/home/userManager/modifyuser/action', methods=["post"])
def modifyAction():
    modifyuid = session.get('muid', None)
    _name = request.form.get('name')
    _dcname = request.form.get('dcname')
    _rank = log.rankEncoder(request.form.get('rank'))
    datas = db_manage.select("users", ["*"], f"WHERE ud={modifyuid}")[0]
    columns = []
    if _name != datas[3]:
        columns.append(f"`name` = '{_name}'")
    if _dcname != datas[4]:
        columns.append(f"`discord_name` = '{_dcname}'")
    if _rank != datas[5]:
        columns.append(f"`rank` = {_rank}")
    if len(columns) > 0:
        modified_columns = ""
        for ci in range(len(columns) - 1):
            column = columns[ci]
            addtext = column + ', '
            modified_columns += addtext
        modified_columns += columns[len(columns) - 1]
        sql = f"UPDATE users SET {modified_columns} WHERE ud={modifyuid}"
        db_manage.execute(sql)
        db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                         f"0, '{session.get('name', None)}', '{_name}', '{modifier.date_string()}', 'mdu'")
    return redirect('/home/userManager')

@app.route('/home/userManager/createUser')
def createSite():
    err = ""
    if session.get("uerr", None) is not None:
        err = session.get("uerr", None)
        session["uerr"] = ""
    return render_template("user_creator.html", error=err)

@app.route('/home/userManager/createUser/action', methods=["post"])
def createUser():
    username = request.form.get('usern')
    password = request.form.get('pasw')
    name = request.form.get('name')
    dcname = request.form.get('dcname')
    rankid = log.rankEncoder(request.form.get('rank'))
    datas = db_manage.select("users", ["*"], "")
    print(username, password, name, dcname, rankid)
    if not modifier.includeMatrix(datas, username) and username != "" and password != "" and name != "":
        db_manage.insert("users", ["`ud`", "`username`", "`password`", "`name`", "`discord_name`", "`rank`"],
                         f"0, '{username}', '{password}', '{name}', '{dcname}', {rankid}")
        db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                         f"0, '{session.get('name', None)}', '{username}', '{modifier.date_string()}', 'cu'")
        if dcname != "":
            webhook.sendWebhook(f"{session.get('name', None)} hozzáférést adott {dcname} felhasználónak az online kezelőfelülethez!", "Felhasználó hozzáadása")
        else:
            webhook.sendWebhook(f"{session.get('name', None)} létrehozta {username} felhasználót az online kezelőfelületen!", "Felhasználó hozzáadása")
        session['usmg'] = "Felhasználó létrehozva!"
        return redirect('/home/userManager/')
    else:
        errortext = ""
        if modifier.includeMatrix(datas, username):
            errortext = "Már regisztráltak felhasználót ezzel a bejelentkezési névvel. Kérlek adj meg másikat!"
        elif username == "":
            errortext = "Kérlek adj meg egy felhasználónevet!"
        elif password == "":
            errortext = "Kérlek adj meg egy jelszót az új felhasználónak!"
        elif name == "":
            errortext = "Kérlek nevezd el a felhasználódat a név mezőben!"
        session['uerr'] = errortext
        return redirect('/home/userManager/createUser')

@app.route('/home/userManager/deluser')
def deleteUser():
    uid = request.args.get('uid')
    if uid != 1:
        rank = session.get('rank')
        deldata = db_manage.select("users", ["*"], f"WHERE `ud`={uid}")[0]
        if deldata[5] < rank:
            db_manage.remove("users", f"ud={uid}")
            db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                             f"0, '{session.get('name', None)}', '{deldata[1]}', '{modifier.date_string()}', 'du'")
            dcname = deldata[4]
            if dcname != "":
                webhook.sendWebhook(f"{session.get('name', None)} hozzáférést adott {dcname} felhasználónak az online kezelőfelülethez!", "Felhasználó törlése")
            else:
                webhook.sendWebhook(f"{session.get('name', None)} létrehozta {deldata[1]} felhasználót az online kezelőfelületen!", "Felhasználó törlése")
            session['umsg'] = "Felhasználó törölve!"
            return redirect('/home/userManager/')
        else:
            session['uer'] = "Sikertelen felhasználóművelet!"
            return redirect('/home/userManager/')

@app.route('/logout')
def logout():
    session['error'] = ""
    session['msg'] = f"Bye, bye {session.get('name', None)}"
    db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                     f"0, '{session.get('name', None)}', '', '{modifier.date_string()}', 'lo'")
    session['name'] = ""
    session['rank'] = 0
    session['order'] = "normal"
    return redirect('/')

if __name__ == "__main__":
    app.run(port=8080)