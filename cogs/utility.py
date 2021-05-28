import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name="createEmbed")
    async def create_embed(self, ctx, title, description, footer):
        """
        SYNTAX: pcreateEmbed "title here" "description here" "footer here"
        """
        embed = discord.Embed(title=title, description=description)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)


def setup(client: commands.Bot):
    client.add_cog(Utility(client))