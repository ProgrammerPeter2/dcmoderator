import discord
from discord import embeds
from discord.utils import get
from discord.ext import commands, tasks
from discord.message import Message
from libs import modifier
import datetime
import os
from libs import db_manage
from libs import mutedate_cal



client = commands.Bot(command_prefix="~")
client.remove_command("help")
badWords = []
mutes = {}
log_channel = client.get_channel(831509478427328522)
guild = client.get_guild(831444546054389760)
moderatorrole = None
speakrole = None
muterole = None

@client.event
async def on_ready():
    print("Bot is ready!")
    global log_channel, guild, moderatorrole, mutes, badWords, speakrole, muterole
    badWords = db_manage.select("badwords", ["*"], "")
    try:
        guild = client.get_guild(831444546054389760)
    except Exception as e:
        print(e)
    log_channel = client.get_channel(831509478427328522)
    speakrole = discord.utils.get(guild.roles, id=834391521917796372)
    muterole = discord.utils.get(guild.roles, id=831484974141407264)
    moderatorrole = discord.utils.get(guild.roles, id=831484977102323712)
    await log_channel.send("Moderátorbot v1.2 elindítva ekkor: " + modifier.date_string())
    unmute.start()
    updateDb.start()

@tasks.loop(seconds=1)
async def unmute():
    global log_channel, mutes, speakrole, muterole
    mutes = db_manage.select("mutes", ["*"], "")
    for mute in mutes:
        if modifier.string_date(mute[2]) < datetime.datetime.now():
            member = await guild.fetch_member(int(mute[1]))
            try:
                await member.add_roles(speakrole)
                await member.remove_roles(muterole)
            except:
                pass
            db_manage.remove("mutes", "id=%s" %mute[0])
            db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                             f"0, 'moderátorbot', '{member}', '{mute[2]}', 'unmute'")
            print(member, "was unmuted.")

@tasks.loop(seconds=10)
async def updateDb():
    global badWords
    bad_words = db_manage.select("badwords", ["*"], "")
    file = open("/app/datas/badWord.txt", "rw", encoding="utf8")
    fileAppender = open("/app/datas/badWord.txt", "a", encoding="utf8")
    if bad_words != []:
        badWords = bad_words
        if file.read().split(",\n") != badWords:
            file.truncate()
            for word in badWords:
                _word = word + ",\n"
                fileAppender.write(_word)
    if bad_words == [] and badWords == []:
        badWords = file.read().split(",\n")

async def get_mutes(channel: discord.TextChannel, author: discord.member.Member, isModerator = False):
    if isModerator:
        await channel.send(f"{author.mention} a némítások adatait elküldöm privátban!")
        mutes = db_manage.select("mutes", ["*"], "")
        if len(mutes) < 1:
            await author.send(f"{modifier.date_string()}: Nincs egy aktív némítás sem!")
        else:
            for mute in mutes:
                member = await guild.fetch_member(int(mute[1]))
                await author.send(f"{member} némítva eddig_ {mute[2]}")
        meanem = embeds.Embed(title="Jelentés", description=f"{author} lekérte az összes aktív némítást!",
                              color=discord.colour.Color.blue())
        meanem.set_author(name=author.display_name, icon_url=author.avatar_url)
        await log_channel.send(embed=meanem)
        print(modifier.date_string(), datetime.datetime.now())
        db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                         f"0, '{author.display_name}', '', '{modifier.date_string()}', 'getmute'")
    else:
        await channel.send(f"{author.mention}! Nincs jogusultságod futtatni ezt a parancsot!")

async def _badwords(channel: discord.TextChannel, author: str):
    badWords = db_manage.select("badwords", ["*"], "")
    text = "Tiltott szavak:\n"
    for badword in badWords:
        word = ""
        for w in badword:
            if w != '(' or w != '\'' or w != ')' or w != ',':
                word += w
        add = word + '\n'
        text += add
    await channel.send(text)
    db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                     f"0, '{author}', '', '{modifier.date_string()}', 'gbw'")

async def clear(channel: discord.TextChannel, author: discord.member.Member, limit=0, isModerator = False):
    if isModerator:
        if limit > 0:
            await channel.purge(limit=limit+1)
            db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                             f"0, '{author}', '{channel}', '{modifier.date_string()}', 'cls {limit+1}'")
        else:
            raise commands.MissingRequiredArgument
    else:
        await channel.send(f"{author.mention}! Nincs jogosultságod futtatni ezt a parancsot!")
        db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                         f"0, '{author.mention}', '{channel}', '{modifier.date_string()}', 'clf mr'")

@client.event
async def on_message(message: Message):
    channel = message.channel
    user = message.author
    words = message.content.lower().split(chr(32))
    global badWords
    is_bad_word = False
    bad_words = list()
    badWord_counter = 0
    badWordTimer = 60
    badWordTime = 0
    try:
        member = await guild.fetch_member(user.id)
        if muterole in member.roles:
            await message.delete()
    except:
        pass
    for word in words:
        badword = ""
        isBadWord = False
        for badWord in badWords:
            if modifier.rem_char(badWord) in word:
                isBadWord = True
                badWord_counter += 1
                badWordTime += badWordTimer
                badword = word
        if isBadWord:
            if not badword in bad_words:
                bad_words.append(badword)
            if not is_bad_word:
                is_bad_word = True
    if is_bad_word and user.name != "moderátor-bot" and not "~" in message.content:
        mutedate = mutedate_cal.calculate(datetime.datetime.now(), badWordTime)
        mdt = modifier.date_string(mutedate)
        db_manage.insert("mutes", ["id", "uid", "mutedate", "uname"], "0, '" + str(user.id) + "' , '" + mdt + "' , '" + user.name + "'")
        bwttext = f"{badWordTime} másodpercre"
        if badWordTime % 60 == 0:
            bwttext = f"{badWordTime//60} percre"
        elif badWordTime > 60 and badWordTime % 60 != 0:
            bwtmin = badWordTime // 60
            bwtsec = badWordTime
            while bwtsec >= 60:
                bwtsec -= 60
            bwttext = f"{bwtmin} percre és {bwtsec} másodpercre"
        embed = discord.embeds.Embed(title="Csúnya beszéd észlelve!", description=f"{user} {bwttext} némítva lett.", timestamp=datetime.datetime.now(), color=0xFF5733)
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.add_field(name="Üzenet:", value=message.content)
        embed.add_field(name="Csúnya szavak száma:", value=str(badWord_counter), inline=False)
        embed.add_field(name="Csúnya szavak:", value=str(bad_words), inline=False)
        await log_channel.send(embed=embed)
        await user.add_roles(muterole)
        await user.remove_roles(speakrole)
        db_manage.insert("logs", ["id", "user", "target", "date", "action"], f"0, 'moderátorbot', '{user}', '{modifier.date_string(mutedate)}', 'mute'")
        await channel.send(f"{user.mention} Ne beszélj csúnyán!")
        await user.send(f"{user.mention} {bwttext} némítva lettél!")
        try:
            await message.delete()
        except:
            pass
    if message.content.startswith('~'):
        isModerator = False
        if moderatorrole in user.roles:
            isModerator = True
        content = message.content
        if content.startswith('~get_mutes'):
            await get_mutes(channel, user, isModerator)
        elif content.startswith('~badwords'):
            await _badwords(channel, user)
        elif content.startswith('~clear'):
            limit = int(content[6:])
            await clear(channel, user, limit, isModerator)
        elif content.startswith('~changelog'):
            changelog = embeds.Embed(title="Fejlesztési infó", description="Itt találod a verzióelőzményeket:", colour=4289797)
            changelog.add_field(name="Beta verziók", value="Moderátor funkciók futtatása", inline=False)
            changelog.add_field(name="Verzió 1.0", value="Logging rendszer, Parancsok bot, webes kezelőfelület béta", inline=False)
            changelog.add_field(name="Verzió 1.1", value="Parancsok-bot beolvasztása a fő botba", inline=False)
            changelog.add_field(name="Verzió 1.2", value="Changelog és help parancsok", inline=False)
            await channel.send(embed=changelog)
        elif content.startswith('~help'):
            helpText = embeds.Embed(title="Parancsok", description="Itt találod a parancsokat!", colour=4289797)
            helpText.add_field(name="Prefix:", value="~")
            helpText.add_field(name="Csak moderátoroknak elérhető:",
                               value="~get_mutes\n Megírja neked az összes aktív némítást!\n~clear\n Kitörli a megadott mennyiségű üzenetet!", inline=False)
            helpText.add_field(name="Általános parancsok:",
                               value="~badwords\n Kiírja az összes tiltott szót!\n~changelog\n Kiírja a verzióelőzményeket!", inline=False)
            await channel.send(embed=helpText)
client.run(str(os.environ['TOKEN']))