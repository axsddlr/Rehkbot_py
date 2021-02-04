import discord
import requests
from datetime import datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


def getValorantGameUpdates():
    URL = "https://api.henrikdev.xyz/valorant/v1/website/en-us?filter=game_updates"

    response = requests.get(URL)
    return response.json()


def getValorantStats():
    URL = "https://api.henrikdev.xyz/valorant/v1/mmr/na/Rehkloos/001"

    response = requests.get(URL)
    return response.json()
    print(URL)


class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Valorant Updates",
                      aliases=['valupdates'],
                      help='Valorant specific commands')
    @commands.cooldown(2, 60, BucketType.user)
    async def valupdates(self, ctx):

        banner = ""
        title = ""
        url = ""
        responseJSON = getValorantGameUpdates()

        # JSON Results Mapping
        banner = responseJSON['data'][0]['banner_url']
        title = responseJSON['data'][0]['title']
        url = responseJSON['data'][0]['url']
        # utc_dt = datetime.strptime(responseJSON['data'][0]['date'], '%Y-%m-%dT%H:%M:%S.%fZ')

        # await ctx.message.channel.send(banner)

        embed = discord.Embed(
            title=title,
            description=url,
            # crimson color code
            colour=(0xDC143C)
        )
        # embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.set_image(url=banner)

        await ctx.send(embed=embed)

    @commands.command(name="Valorant Rank ",
                      aliases=['valrank'],
                      help='Valorant specific commands')
    @commands.cooldown(2, 60, BucketType.user)
    async def valstats(self, ctx):

        responseJSON = getValorantStats()
        rank = responseJSON['data']['currenttierpatched']
        elo = responseJSON['data']['elo']

        await ctx.message.channel.send("Rank: " + str(rank) + " | " + "Elo: " + str(elo))


def setup(bot):
    bot.add_cog(Valorant(bot))
