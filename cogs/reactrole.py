import discord
from discord.ext import commands
from utils.json_loader import read_json, write_json
import json
class ReactionRole(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def reactrole(self, ctx, emoji, role: discord.Role, *, message):

        emb = discord.Embed(description=message)
        msg = await ctx.channel.send(embed=emb)
        await msg.add_reaction(emoji)

        
        data = read_json("reactrole")

        new_react_role = {
            'role_name': role.name, 
            'role_id': role.id,
            'emoji': emoji,
            'message_id': msg.id}

        data.append(new_react_role)
        write_json(data, "reactrole")

        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.member.bot:
            pass

        else:
            
            data = read_json("reactrole")
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(self.bot.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        data = read_json("reactrole")
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(self.bot.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                    
                await self.bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

def setup(bot):
    bot.add_cog(ReactionRole(bot))