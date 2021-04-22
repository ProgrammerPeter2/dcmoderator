from discord.ext import commands
import datetime
from moderator import modifier
import os
import json

client = commands.Bot(command_prefix="~")
guild = client.get_guild(831444546054389760)
config = json.load(open("/app/datas/config.json", "r", encoding="utf8"))
userDatas = json.load(open("/app/datas/users.json", "r", encoding="utf8"))

@client.event
async def on_ready():
    global config, userDatas, guild
    guild = client.get_guild(831444546054389760)
    os.chdir("datas")
    print("ready!")

@client.command()
async def start_manage(ctx):
    log_channel = client.get_channel(831509478427328522)
    global guild
    await log_channel.send("Role system is running!")
    config = json.load(open("/app/datas/config.json", "r", encoding="utf8"))
    userDatas = json.load(open("/app/datas/users.json", "r", encoding="utf8"))
    while not client.is_closed():
        with open("mutes.txt", "r", encoding="utf8") as file:
            content = file.read().split(",")
        if len(content) >= 3:
            for cind in range(1, len(content), 2):
                if modifier.string_date(content[cind+1]) < datetime.datetime.now():
                    uid = int(content[cind])
                    member = await guild.fetch_member(uid)
                    roles = userDatas[member.name]["roles"]
                    await member.remove_roles(guild.get_role(config["roles"]["némítva"]))
                    await member.add_roles(guild.get_role(config["roles"]["beszélhet"]))
                    if not guild.get_role(config["roles"]["rendszergazda"]) in member.roles:
                        for role in roles:
                            if not role in member.roles:
                                add_role = guild.get_role(config["roles"][role])
                                try:
                                    await member.add_roles(add_role)
                                except Exception:
                                    pass
                    if len(content) <= 3:
                        content.clear()
                    else:
                        content.pop(cind)
                        content.pop(cind+1)
                    with open("mutes.txt", "w", encoding="utf8") as file:
                        if len(content) > 0:
                            file.truncate()
                            text = ","
                            for c in content:
                                add_text = c + ","
                                text += add_text
                            file.write(text)

@client.command()
async def get_content(ctx):
    with open("mutes.txt", "r", encoding="utf8") as file:
        await ctx.send(file.read())

client.run("ODMzNjc0OTQyNDAyNzg5NDE3.YH1ySw.FEUwu-AiKAU12xsbZLWKlitUsa4")