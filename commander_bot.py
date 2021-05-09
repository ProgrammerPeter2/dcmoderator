import discord
from datetime import datetime
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
                await ctx.author.send(f"{member} némítva eddig_ {mute[2]}")
        meanem = embeds.Embed(title="Jelentés", description=f"{ctx.author} lekérte az összes aktív némítást!",
                              color=discord.colour.Color.blue())
        meanem.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await log_channel.send(embed=meanem)
        print(modifier.date_string(), datetime.now())
        db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                         f"0, '{ctx.author}', '', '{modifier.date_string()}', 'getmute'")
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
    db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                     f"0, '{ctx.author}', '', '{modifier.date_string()}', 'gbw'")

@client.event
async def on_command_error(error, ctx:Context):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Nem adtad meg az összes paramétert!")

@client.command()
async def clear(ctx: Context, limit=0):
    if moderatorrole in ctx.author.roles:
        if limit > 0:
            await ctx.channel.purge(limit=limit)
            db_manage.insert("logs", ["id", "user", "target", "date", "action"],
                             f"0, '{ctx.author}', '{ctx.channel}', '{modifier.date_string()}', 'clear'")
        else:
            raise commands.MissingRequiredArgument
    else:
        await ctx.send(f"{ctx.author.mention}! Nincs jogosultságod futtatni ezt a parancsot!")

client.run("ODM4NDAzMjk0NDY0MTgxMjc1.YI6l6g.IInc1pZqdN92JIY-rrXHIOA8FB0")