import discord
from discord.ext import commands
from time import sleep
import mutedate_cal
from datetime import datetime

class Muter:
    def __init__(self, client: commands.Bot, mutes, time):
        self.client = client
        self.channel = self.client.get_channel(831509478427328522)
        self.mutes = mutes
        self.time = time
        self.date = mutedate_cal.calculate(datetime.now(), self.time)
        self.mutes = open("datas/mutes.txt", "r", encoding="utf8").read().split(",")
    
    async def on_message(self, message):
        for mute_ind in range(0,len(self.mutes),2):
            muteuser = self.mutes[mute_ind]
            print(muteuser, type(muteuser))