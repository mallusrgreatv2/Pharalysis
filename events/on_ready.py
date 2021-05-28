import discord
from discord.ext import commands
import time
from pathlib import Path
import json

cwd = Path(__file__).parents[0]
cwd = str(cwd)

class OnReady(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot Ready | {self.client.user.id}')
        global start_time
        start_time = time.time()
        data = read_json("blacklists")
    
def setup(client):
    client.add_cog(OnReady(client))

def read_json(filename):
    with open(f"{cwd}/Dicts/{filename}.json", "r") as file:
        data = json.load(file)

    return data

def write_json(data, filename):
    with open(f"{cwd}/Dicts/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)