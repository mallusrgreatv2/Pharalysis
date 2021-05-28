from events.on_ready import read_json, write_json
import discord
from discord.ext import commands
import io
import contextlib
import textwrap
from discord import Message
from discord.ext.commands.help import Paginator
class OwnerCommands(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.command(name="blacklist")
    @commands.is_owner()
    async def blacklist(self, ctx: Message, user: discord.User):
        self.client.blacklisted_users.append(user.id)
        data = read_json("blacklists")
        data["blacklisted_users"].append(user.id)
        write_json(data, "blacklists")
        await ctx.send(f"Unblacklisted {user.name}")

    @commands.command(name="unblacklist")
    @commands.is_owner()
    async def unblacklist(self, ctx: Message, user: discord.User):
        self.client.blacklisted_users.remove(user.id)
        data = read_json("blacklists")
        data["blacklisted_users"].remove(user.id)
        write_json(data, "blacklists")
        await ctx.send(f"Unblacklisted {user.name}")
        


def setup(client:commands.Bot):
    client.add_cog(OwnerCommands(client))