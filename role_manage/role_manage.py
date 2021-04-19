from discord.ext import commands

class RoleManage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog: Role_management is loaded!")

def setup(client):
    client.add_cog(RoleManage(client))