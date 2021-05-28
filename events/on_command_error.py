import discord
from discord.ext import commands
import datetime, time

class OnCommandError(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored =(commands.CommandNotFound)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} command was disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can only be used in guilds.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'Bad arguments for command {ctx.command}')

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Required arguments are missing.')

    
def setup(client):
    client.add_cog(OnCommandError(client))