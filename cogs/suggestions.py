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
    async def suggest(self, ctx, *, suggestion):
        data = read_json("suggestion")
        data = data[f"{ctx.guild.id}"]
        if not data:
            await ctx.send("No suggestion channel found. `{p}setSuggestionChannel #channel`")
            return
        
        channel = self.bot.get_channel(f"{data}")
        emb = discord.Embed(title="New Suggestion!",
                            description=suggestion)
        emb.set_footer(text=f"Suggested by {ctx.author.name}#{ctx.author.discriminator}")

        msg = await channel.send(embed = emb)
        msg.add_reaction("✅")
        msg.add_reaction("x")
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Suggestions(bot))
