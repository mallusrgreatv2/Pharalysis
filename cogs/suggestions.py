import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Cog, Bot, command
from utils.util import GetMessage
from utils.json_loader import read_json, write_json


class Suggestions(Cog):
    def __init__(self, bot) -> None:
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setSuggestionChannel(self, ctx, channel: discord.TextChannel):
        try:
            data = read_json("suggestion")
            data[f"{ctx.guild.id}"] = channel.id
            self.bot.suggestions[f"{ctx.guild.id}"] = channel.id
            write_json(data, "suggestion")
            await ctx.send(f"Set {channel.mention} as suggestion channel.")
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def suggest(self, ctx):
        data = read_json("suggestion")
        data = data[f"{ctx.guild.id}"]
        if not data:
            await ctx.send("No suggestion channel found. `{p}setSuggestionChannel #channel`")
            return
        channel: discord.TextChannel = self.bot.get_channel(data)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        embed = discord.Embed(title="Suggestion",
                              description="Share your suggestion below!")
        embed.set_footer(text="Type 'cancel' to cancel.")
        sent = await ctx.send(embed=embed)
        try:
            response = await self.bot.wait_for('message', check=check, timeout=15)
        except asyncio.TimeoutError:
            await ctx.send("Suggestion timed out.")
        
        if response.content.lower() == 'cancel':
            await ctx.send("Cancelled the suggestion.", delete_after=6)
            await response.delete()
            await sent.delete()
            await ctx.message.delete()  
            return

        emb = discord.Embed(title="New Suggestion!",
                            description=response.content)
        emb.set_footer(text=f"Suggested by {ctx.author.name}")

        await channel.send(embed = emb)
        await response.delete()
        await sent.delete()
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Suggestions(bot))
