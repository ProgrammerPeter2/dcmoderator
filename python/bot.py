import discord
from discord.ext import commands
import discord.message
import modifier
import datetime
import mutedate_cal
import json

client = commands.Bot(command_prefix='??')
mutes = []
badWords = open("datas/badWord.txt", "r", encoding="utf8").read().split(",\n")
log_channel = client.get_channel(831509478427328522)
guild = client.get_guild(831444546054389760)

@client.event
async def on_ready():
    print("Bot is ready!")
    global log_channel, guild, mutes
    guild = client.get_guild(831444546054389760)
    log_channel = client.get_channel(831509478427328522)
    await log_channel.send("teszt")
    for i in open("datas/users.txt", "r", encoding="utf8").read().split(",\n"):
        userList = [i, ""]
        mutes.append(userList)
    print(mutes)

@client.event
async def on_message(message):
    channel = message.channel
    user = message.author
    words = message.content.lower().split(chr(32))
    global badWords, mutes, log_channel
    mute = False
    for i in range(0, len(mutes)):
        if user.name == mutes[i][0] and not mutes[i][1] == "":
            if modifier.string_date(mutes[i][1]) > datetime.datetime.now():
                try:
                    await message.delete()
                except:
                    pass
                mute = True
            elif modifier.string_date(mutes[i][1]) <= datetime.datetime.now():
                mutes[i][1] = ""
                print(mutes[i])
    if not mute:
        is_bad_word = False
        bad_words = list()
        badWord_counter = 0
        for word in words:
            badword = ""
            isBadWord = False
            for badWord in badWords:
                if badWord in word:
                    isBadWord = True
                    badWord_counter += 1
                    badword = word
            if isBadWord:
                if not badword in bad_words:
                    bad_words.append(badword)
                if not is_bad_word:
                    is_bad_word = True
        if is_bad_word:
            embed = discord.embeds.Embed(title="Csúnya szó észlelve!", color=discord.Color.red())
            embed.set_author(name="Moderátor riasztás", icon_url=user.avatar_url)
            embed.add_field(name="Felhasználó:", value=user.name)
            embed.add_field(name="Üzenet:", value=message.content)
            embed.add_field(name="Csúnya szavak száma:", value=str(badWord_counter))
            embed.add_field(name="Csúnya szavak:", value=str(bad_words))
            config = json.load(open("datas/config.json", "r"))["badWordTime"]
            mutedate = mutedate_cal.calculate(datetime.datetime.now(), (config * badWord_counter))
            for i in range(0, len(mutes)):
                if mutes[i][0] == user.name:
                    mutes[i][1] = modifier.date_string(mutedate)
            await log_channel.send(embed=embed)
            await channel.send(f"{user.name} Ne beszélj csúnyán!")
            await user.send(f"{user.name} {badWord_counter * config} másodpercre némítva lettél!")
            try:
                await message.delete()
            except:
                pass

client.run("ODEyMzM2MDMwMjI5MjAwOTA2.YC_Q4g.Bcj8mWFC4db7yxN1PNC3wMoXKBM")