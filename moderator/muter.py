from discord.ext import commands
import bot
import modifier
from datetime import datetime
import json

class Muter(commands.Cog):
    def __init__(self):
        self.client = bot.client
        self.channel = self.client.get_channel(831509478427328522)
        self.mutes = bot.mutes
        self.users = ""
        self.path = bot.path
        config = json.load(open((self.path+"/config.json"), "r", encoding="utf8"))
        users = json.load(open((self.path+"/users.json"), "r", encoding="utf8"))
        while True:
            for user in self.mutes:
                if modifier.string_date(user[1]) > datetime.datetime.now():
                    roles = users[user][roles]
                    for role in roles:
                        r = config["roles"][role]
                        member = bot.guild.get_member_named(user)
                        print(type(member))

    def setMutes(self, mutes):
        self.mutes = mutes

def setup(bot):
    bot.add_cog(Muter())