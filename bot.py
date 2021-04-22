import discord
from discord.ext import commands
from discord.message import Message
from moderator import modifier
import datetime
from moderator import mutedate_cal
import json
from moderator import mutes

client = commands.Bot(command_prefix='/')
import os
os.chdir("..")
path = "\datas"
badWords = open("/app/datas/badWord.txt", "r", encoding="utf8").read().split(",\n")
config = json.load(open("/app/datas/config.json", "r", encoding="utf8"))
log_channel = client.get_channel(831509478427328522)
guild = client.get_guild(831444546054389760)

@client.event
async def on_ready():
    print("Bot is ready!")
    global log_channel, guild, config, mutes
    guild = client.get_guild(831444546054389760)
    log_channel = client.get_channel(831509478427328522)
    await log_channel.send("teszt")

@client.event
async def on_message(message: Message):
    channel = message.channel
    user = message.author
    words = message.content.lower().split(chr(32))
    global badWords, log_channel, config, guild
    is_bad_word = False
    bad_words = list()
    badWord_counter = 0
    try:
        member = await guild.fetch_member(user.id)
        if guild.get_role(config["roles"]["némítva"]) in member.roles:
            try:
                await message.delete()
            except:
                pass
    except:
        pass
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
        badWordTimer = config["badWordTime"]
        mutedate = mutedate_cal.calculate(datetime.datetime.now(), (badWordTimer * badWord_counter))
        mutetext = "," + str(user.id) + "," + modifier.date_string(mutedate)
        mutes.add_to_mutes(mutetext)
        speakrole = guild.get_role(config["roles"]["beszélhet"])
        muterole = guild.get_role(config["roles"]["némítva"])
        await user.add_roles(muterole)
        await user.remove_roles(speakrole)
        await log_channel.send(embed=embed)
        await channel.send(f"{user.mention} Ne beszélj csúnyán!")
        await user.send(f"{user.mention} {badWord_counter * badWordTimer} másodpercre némítva lettél!")
        try:
            await message.delete()
        except:
            pass
client.run("ODEyMzM2MDMwMjI5MjAwOTA2.YC_Q4g.Bcj8mWFC4db7yxN1PNC3wMoXKBM")