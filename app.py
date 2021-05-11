from flask import *
import db_manage
import logMaker as log
import modifier
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
    user_datas = db_manage.select("users", ["*"], "")
    ip = request.environ['REMOTE_ADDR']
    loggedIn = False
    username = ""
    for user in user_datas:
        if user[1] == uname and user[2] == passw:
            loggedIn = True
            username = user[3]
    if loggedIn:
        session['name'] = username
        db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                         f"0, '{username}', '', '{modifier.date_string()}', 'lis'")
        return redirect(location='/home')
    else:
        db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                         f"0, '{ip}', '', '', 'lif'")
        session['error'] = "Something went wrong with your login datas!"
        return redirect(location="/")

@app.route('/home')
def home():
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
    for word in badWords:
        badwords.append(modifier.rem_char(word))
    return render_template("home.html", user=session.get('name', None), datas=mutes, logs=logData, words=badwords)

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
    return render_template("logs.html", logs=logData)

@app.route('/la', methods=["post"])
def logs_action():
    order = request.form.get('order')
    if order == "Régebbiek elől":
        session['order'] = ""
    elif order == "Nem túl régi esmények elől":
        session['order'] = "normal"
    return redirect('/home/logs')

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
        webhook.sendWebhook(text)
        db_manage.insert("badwords", ['badword'], f"'{word}'")
        db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                         f"0, '{session.get('name', None)}', '{word}', '{modifier.date_string()}', 'abw'")
    else:
        session["bwerr"] = "A szó már szerepel a listában. Kérlek adj meg egy másik szót!"
        _redirect = '/home/new_badWord'
    return redirect('/home')

@app.route('/logout')
def logout():
    session['error'] = ""
    session['msg'] = f"Bye, bye {session.get('name', None)}"
    db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                     f"0, '{session.get('name', None)}', '', '{modifier.date_string()}', 'lo'")
    session['name'] = ""
    session['order'] = "normal"
    return redirect('/')

if __name__ == "__main__":
    app.run(port=8080)