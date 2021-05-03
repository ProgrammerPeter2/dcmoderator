import discord
import asyncio
from discord.ext import commands
from discord.ext.commands.context import Context
from discord import embeds
from libs import db_manage
from libs import modifier

client = commands.Bot(command_prefix="~")
guild = client.get_guild(831444546054389760)
log_channel = client.get_channel(831509478427328522)
moderatorrole = None

@client.event
async def on_ready():
    global guild, log_channel, moderatorrole
    guild = client.get_guild(831444546054389760)
    log_channel = client.get_channel(831509478427328522)
    moderatorrole = guild.get_role(831484977102323712)
    await log_channel.send("Moderátorbot parancsai betöltve!")
    print("Moderatorbot-commands was loaded!")

@client.command()
async def get_mutes(ctx: Context):
    if moderatorrole in ctx.author.roles:
        _channel = ctx.channel
        await _channel.send(f"{ctx.author.mention} a némítások adatait elküldöm privátban!")
        mutes = db_manage.select("mutes", ["*"], "")
        if len(mutes) < 1:
            await ctx.author.send(f"{modifier.date_string()}: Nincs egy aktív némítás sem!")
        else:
            for mute in mutes:
                member = await guild.fetch_member(int(mute[1]))
                await ctx.author.send(f"{member} némítva eddig_ {modifier}")
        meanem = embeds.Embed(title="Jelentés", description=f"{ctx.author} lekérte az összes aktív némítást!",
                              color=discord.colour.Color.blue())
        meanem.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await log_channel.send(embed=meanem)
    else:
        await ctx.send(f"{ctx.author.mention}! Nincs jogusultságod futtatni ezt a parancsot!")

@client.command()
async def badWords(ctx: Context):
    badWords = db_manage.select("badwords", ["*"], "")
    await ctx.channel.send("Tiltott szavak:")
    for badword in badWords:
        word = ""
        for w in badword:
            if w != '(' or w != '\'' or w != ')' or w != ',':
                word += w
        await ctx.send(word)

@client.event
async def on_command_error(error, ctx:Context):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Nem adtad meg az összes paramétert!")

@client.command()
async def addword(ctx: Context, word=""):
    if moderatorrole in ctx.author.roles:
        if word != "":
            badWords = db_manage.select("badwords", ["*"], "")
            print(badWords)
            if not word in badWords:
                await ctx.send("Tiltott szó hozzáadva")
                meanem = embeds.Embed(title="Jelentés", description=f"{ctx.author} hozzáadot egy új tiltott szót!",
                                      colour=discord.colour.Color.blue())
                meanem.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
                meanem.add_field(name="Tiltott szó:", value=word)
                await log_channel.send(embed=meanem)
            else:
                await ctx.send("Ez a szó már szerepel a listán")
        else:
            await ctx.send("Nem adtál meg szavat!")
    else:
        await ctx.send(f"{ctx.author.mention}! Nincs jogosultságod futtatni ezt a parancsot!")

@client.command()
async def clear(ctx: Context, limit=0):
    if moderatorrole in ctx.author.roles:
        if limit > 0:
            await ctx.channel.purge(limit=limit)
        else:
            raise commands.MissingRequiredArgument
    else:
        await ctx.send(f"{ctx.author.mention}! Nincs jogosultságod futtatni ezt a parancsot!")

client.run("ODM4NDAzMjk0NDY0MTgxMjc1.YI6l6g.IInc1pZqdN92JIY-rrXHIOA8FB0")