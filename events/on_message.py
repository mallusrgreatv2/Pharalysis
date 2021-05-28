import discord
from discord.ext import commands
import json

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener
    async def on_message(self, message: discord.Message):
        if message.author.id == self.client.user.id:
            return
        
        if message.author.id in self.client.blacklisted_users:
            return

        await self.client.process_commands()

    
def setup(client):
    client.add_cog(Events(client))

