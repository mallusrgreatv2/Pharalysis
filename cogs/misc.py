import asyncio
import platform
import discord
from discord.ext import commands
from cogs.Giveaways import convert
import random
import giphy_client
from giphy_client.rest import ApiException



class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(
        name="stats", description="A useful command that displays bot statistics."
    )
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(
            title=f"{self.bot.user.name} Stats",
            description="\uFEFF",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,
        )

        embed.add_field(name="Bot Version:", value=self.bot.version)
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="Discord.Py Version", value=dpyVersion)
        embed.add_field(name="Total Guilds:", value=serverCount)
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="Bot Developers:", value="<@700397009336533032> | mallusrgreat#6991")

        embed.set_footer(text=f"Carpe Noctem | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(
        name="echo",
        description="A simple command that repeats the users input back to them.",
    )
    async def echo(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
            title="Please tell me what you want me to repeat!",
            description="||This request will timeout after 1 minute.||",
        )
        sent = await ctx.send(embed=embed)

        try:
            msg = await self.bot.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                and message.channel == ctx.channel,
            )
            if msg:
                await sent.delete()
                await msg.delete()
                await ctx.send(msg.content)
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Cancelling", delete_after=10)

    @commands.command(name="toggle", description="Enable or disable a command!")
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        command = self.bot.get_command(command)

        if command is None:
            await ctx.send("I can't find a command with that name!")

        elif ctx.command == command:
            await ctx.send("You cannot disable this command.")

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send(f"I have {ternary} {command.qualified_name} for you!")
        
    @commands.command()
    async def timer(self, ctx: commands.Context, time):
        _time = convert(time)
        try:
            secondint = _time
            if secondint <= 0 or secondint > 300:
                await ctx.send("Don't try to scam me")
                return
            embed = discord.Embed(title = "Timer", description = f"Ends in {_time} seconds")
            message = await ctx.send(embed = embed)
            while True:
                secondint -= 7
                if secondint <= 0:
                    await ctx.send(f"{ctx.author.mention}, Your timer ended!")
                    break
                editembed = discord.Embed(title = "Timer", description = f"Ends in {secondint}")
                await message.edit(embed = editembed)
                await asyncio.sleep(1)
        except Exception as e:
            await ctx.send(e)



    @commands.command()
    async def gif(self, ctx,*,q="random"):

        api_key=self.bot.giphy_api_key
        api_instance = giphy_client.DefaultApi()

        try: 
        # Search Endpoint
            
            api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
            lst = list(api_response.data)
            giff = random.choice(lst)

            emb = discord.Embed(title=q)
            emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')

            await ctx.channel.send(embed=emb)
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)


def setup(bot):
    bot.add_cog(Misc(bot))
