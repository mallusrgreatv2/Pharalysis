import discord
from discord.ext import commands
import datetime, time

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Help - Commands", description="Write `phelp <command>` for more information about the command.")
        embed.add_field(name='Help', value="`help`")
        await ctx.send(embed)
    
def setup(client):
    client.add_cog(Help(client))