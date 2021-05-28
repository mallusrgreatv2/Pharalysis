import discord
from discord.ext import commands
import os
from cogs.on_ready import read_json

client = commands.AutoShardedBot(command_prefix = 'p', description="Pharalysis bot made for mallusrgreat to learn Python!")

client.blacklisted_users = []
@client.event
async def on_message(message: discord.Message):
        data = read_json("blacklists")
        if message.author.id == client.user.id:
            return
        
        if message.author.id in client.blacklisted_users:
            return
        
        if message.content.lower() == "shh":
            await message.channel.send(message.author.id) 
        
        await client.process_commands(message=message)

client.remove_command('help')
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

       


client.run('ODQxOTg3MzYyMjk2Mjk5NTMx.YJuv1g.3fvJkD2E-WJUkqi1vKCZYLsE2iI')