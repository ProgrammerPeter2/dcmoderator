from discord.ext import commands
import datetime
from moderator import modifier
from moderator import mutes
import os
import json

client = commands.Bot(command_prefix="~")
guild = client.get_guild(831444546054389760)
config = json.load(open("/app/datas/config.json", "r", encoding="utf8"))
userDatas = json.load(open("/app/datas/users.json", "r", encoding="utf8"))
log_channel = client.get_channel(831509478427328522)
roles = []

#@client.event
#async def on_ready():
    #global config, userDatas, guild, roles, log_channel
    #guild = client.get_guild(831444546054389760)
    #moderator = guild.get_role(config["roles"]["moderátor"])
    #rendszergazda = guild.get_role(config["roles"]["rendszergazda"])
    #roles.append(moderator)
    #log_channel = client.get_channel(831509478427328522)
    #roles.append(rendszergazda)
    #os.chdir("datas")
    #print("Role system is ready for work!")

@client.event
async def on_ready():
    global config, guild, roles, log_channel, client
    guild = client.get_guild(831444546054389760)
    moderator = guild.get_role(config["roles"]["moderátor"])
    rendszergazda = guild.get_role(config["roles"]["rendszergazda"])
    roles.append(moderator)
    log_channel = client.get_channel(831509478427328522)
    roles.append(rendszergazda)
    await client.wait_until_ready()
    await log_channel.send("Role system is running!")
    config = json.load(open("/app/datas/config.json", "r", encoding="utf8"))
    while not client.is_closed():
        content = mutes.get_mutes()
        if len(content) >= 3:
            for cind in range(0, len(content), 2):
                if modifier.string_date(content[cind+1]) < datetime.datetime.now():
                    uid = int(content[cind])
                    member = await guild.fetch_member(uid)
                    await member.remove_roles(guild.get_role(config["roles"]["némítva"]))
                    await member.add_roles(guild.get_role(config["roles"]["beszélhet"]))
                    if len(content) <= 3:
                        content.clear()
                    else:
                        content.pop(cind)
                        content.pop(cind+1)
                    mutes.set_mutes(content)


@client.command()
async def get_content(ctx):
    global guild, log_channel, config, roles
    if roles[0] in ctx.author.roles or roles[1] in ctx.author.roles:
        user = ctx.author
        await user.send("Az összes némított felhasználó listázva. Időpont: " + modifier.date_string())
        for mute in mutes.get_mutes():
            userdatas = mute.split(",")
            muser = await guild.fetch_user(int(userdatas[0]))
            await user.send(f"{muser.name} némítva eddig: {userdatas[1]}")
    else:
        await ctx.send(f"{ctx.author.mention} nincs jogosultságod megtekinteni a némíások adatait!")

@client.command()
async def clear(ctx):
    global guild, log_channel, config, roles
    if roles[0] in ctx.author.roles or roles[1] in ctx.author.roles:
        mutes.clear_mutes()
        await ctx.send("Mutes was cleared!")
        await log_channel.send(f"{ctx.author.name} törlölte az összes némítást!")
    else:
        await ctx.send(f"{ctx.author.mention}! Nem tudod törölni a némítástokat, mivel nincsen jogosultságod!")
        await log_channel.send(f"{ctx.author.name} megpróbálta törölni a némításokat de nem volt jogosultsága hozzá!")

client.run("ODMzNjc0OTQyNDAyNzg5NDE3.YH1ySw.FEUwu-AiKAU12xsbZLWKlitUsa4")