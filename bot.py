import discord
from discord.ext import commands
import os

client = commands.AutoShardedBot(command_prefix = 'p', description="Pharalysis bot made for mallusrgreat to learn Python!")
client.remove_command('help')
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run('ODQxOTg3MzYyMjk2Mjk5NTMx.YJuv1g.3fvJkD2E-WJUkqi1vKCZYLsE2iI')