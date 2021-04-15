import discord
from discord.ext import commands
import mutedate_cal as mutecal
import os
import modifier
import datetime
import muter

client = commands.Bot(command_prefix='??')

@client.event
async def on_ready():
    print("Bot is ready!")
    log_channel = client.get_channel(831509478427328522)
    msg = "A program indítása: " + modifier.date_string() + "\n verzió: " + os.getenv("version")
    await log_channel.send("teszt")

@client.event
async def on_message(message):
    channel = message.channel
    user = message.author
    log_channel = client.get_channel(831509478427328522)
    words = message.content.lower().split(chr(32))
    badWords = ["buzi", "kurva", "fasz", "rohadék", "geci"]
    is_bad_word = False
    bad_words = list()
    badWord_counter = 0
    badWord_timer = 0
    badword = ""
    for word in words:
        isBadWord = False
        for badWord in badWords:
            if word == badWord:
                isBadWord = True
                badWord_timer += 60
                badword = word
        if isBadWord:
            badWord_counter += 1
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
        mutecal.calculate(user,datetime.datetime.now(), badWord_timer)
        await log_channel.send(embed=embed)
        await channel.send(f"{user.name} Ne beszélj csúnyán!")
        _muter = muter.Muter(client, user, badWord_timer)
        await message.delete()

@client.command()
async def test(ctx):
    print("Teszt!")
    await ctx.send("Hi! This is a test!")

client.run("ODEyMzM2MDMwMjI5MjAwOTA2.YC_Q4g.Bcj8mWFC4db7yxN1PNC3wMoXKBM")