import discord
from discord.ext import commands
from utils.json_loader import read_json, write_json

class ReactionRole(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="reactionrole", aliases = ["rr", "reactrole", "reactionr", "rrole"])
    async def reactionrole(self, ctx, role: discord.Role, emoji: discord.Emoji, *, message: str):
        emb = discord.Embed(description = message)
        msg = await ctx.send(embed = emb)
        await msg.add_reaction(emoji)
        data = read_json("reactrole")
        new_react_role = {
            'role_name': role.name,
            'role_id': role.id,
            'emoji': emoji,
            'message_id': msg.id
        }
        data.append(new_react_role)
        self.bot.react_role.append(new_react_role)
        write_json(data, "reactrole")

def setup(bot):
    bot.add_cog(ReactionRole(bot))