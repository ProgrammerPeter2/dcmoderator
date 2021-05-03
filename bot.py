import discord
from discord.ext import commands, tasks
from discord.message import Message
from libs import modifier
import datetime
from libs import db_manage
from libs import mutedate_cal



client = commands.Bot(command_prefix="~")
badWords = []
mutes = {}
log_channel = client.get_channel(831509478427328522)
guild = client.get_guild(831444546054389760)
speakrole = None
muterole = None

@client.event
async def on_ready():
    print("Bot is ready!")
    global log_channel, guild, config, mutes, badWords, speakrole, muterole
    badWords = db_manage.select("badWords", ["*"], "")
    config = db_manage.select("config", ["*"], "")
    guild = client.get_guild(831444546054389760)
    log_channel = client.get_channel(831509478427328522)
    speakrole = guild.get_role(834391521917796372)
    muterole = guild.get_role(831484974141407264)
    await log_channel.send("Moderátorbot v1.0 elindítva ekkor: " + modifier.date_string())
    bgtest.start()

@tasks.loop(seconds=1)
async def bgtest():
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
            print(member, "was unmuted.")

@client.event
async def on_message(message: Message):
    channel = message.channel
    user = message.author
    words = message.content.lower().split(chr(32))
    global badWords, log_channel, config, guild, speakrole, muterole
    is_bad_word = False
    bad_words = list()
    badWord_counter = 0
    badWordTimer = 20
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
            if badWord in word:
                isBadWord = True
                badWord_counter += 1
                badWordTime += badWordTimer
                badword = word
        if isBadWord:
            if not badword in bad_words:
                bad_words.append(badword)
            if not is_bad_word:
                is_bad_word = True
    if is_bad_word and user.name != "moderátor-parancsok" and not "~" in message.content:
        mutedate = mutedate_cal.calculate(datetime.datetime.now(), badWordTime)
        mdt = modifier.date_string(mutedate)
        db_manage.insert("mutes", ["id", "uid", "mutedate"], "0, '" + str(user.id) + "' , '" + mdt + "'")
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
        await channel.send(f"{user.mention} Ne beszélj csúnyán!")
        await user.send(f"{user.mention} {badWordTime} másodpercre némítva lettél!")
        try:
            await message.delete()
        except:
            pass
client.run("ODM2ODkzMzA4MDEyNzI0MjU0.YIknoQ.ARQhKKk-hEnlU53qK0yY8rXI59A")