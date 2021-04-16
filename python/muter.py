import discord
from discord.ext import commands
from time import sleep
import mutedate_cal
from datetime import datetime

class Muter:
    def __init__(self, client: commands.Bot, user, time):
        self.client = client
        self.channel = self.client.get_channel(831509478427328522)
        self.user = user
        self.time = time
        self.date = mutedate_cal.calculate(self.user, datetime.now(), self.time)
    
    @self.client.event
    async def on_message(self, message):
        if message.author == self.user:
            print("Beszédkísérlet!")