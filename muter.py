import discord
from discord.ext import commands
from time import sleep

class Muter:
    def __init__(self, client: commands.Bot, user, time):
        self.client = client
        self.channel = self.client.get_channel(831509478427328522)
        self.user = user
        self.time = time
        sleep(self.time)
        message = user + " " + str(time) + "idő után újra beszélhet!"
        await self.channel.send(message)