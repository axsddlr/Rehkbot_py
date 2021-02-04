import discord
import requests
from datetime import datetime
from urllib.parse import unquote
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


def getValorantGameUpdates():
    URL = "https://api.henrikdev.xyz/valorant/v1/website/en-us?filter=game_updates"
    response = requests.get(URL)
    return response.json()


def getValorantRank(Name, Tag):
    URL = "https://api.henrikdev.xyz/valorant/v1/mmr/na/" + Name + "/" + Tag
    response = requests.get(URL)
    return response.json()


def getValorantStats(Name, Tag):
    URL = "https://api.henrikdev.xyz/valorant/v1/profile/" + Name + "/" + Tag
    response = requests.get(URL)
    return response.json()

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #  Valorant News
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

        embed = discord.Embed(
            title=title,
            description=url,
            # crimson color code
            colour=(0xDC143C)
        )
        embed.set_image(url=banner)

        await ctx.send(embed=embed)

    @commands.command(name="Valorant Rank ",
                      aliases=['valrank'],
                      help='Valorant specific commands')
    # @commands.cooldown(2, 60, BucketType.user)
    async def valrank(self, ctx, Name: str = "", Tag: str = ""):

        responseJSON = getValorantRank(Name, Tag)

        # Check if profile exists or is public
        status = responseJSON['status']
        if status == '200':
            riotid = Name + "#" + Tag
            rank = responseJSON['data']['currenttierpatched']
            elo = responseJSON['data']['elo']

            await ctx.message.reply("Rank: " + str(rank) + " | " + "Elo: " + str(elo))
            #  If it does not exist or is private
        elif status == '451':
            message = responseJSON['message']
            await ctx.message.reply(message)
        elif status == '404':
            message = responseJSON['message']
            await ctx.message.reply(message)

    @commands.command(name="Valorant Stats ",
                      aliases=['valstats'],
                      help='Valorant specific commands')
    # @commands.cooldown(2, 60, BucketType.user)
    async def valstats(self, ctx, Name: str = "", Tag: str = ""):

            responseJSON = getValorantStats(Name, Tag)

            # Check if profile exists or is public
            status = responseJSON['status']
            if status == '200':
                riotid = Name + "#" + Tag
                kills = responseJSON['stats']['kills']
                deaths = responseJSON['stats']['deaths']
                kdr = responseJSON['stats']['kdratio']
                wins = responseJSON['stats']['wins']
                winr = responseJSON['stats']['winpercentage']
                TTP = responseJSON['stats']['playtime']['playtimepatched']

                await ctx.message.reply("Total Time Played: " + str(TTP) + " | Wins: " + str(wins) + " | Win/Loss: " + str(winr) + " | Kills: " + str(kills) + " | KDR: " + str(kdr) + " | Deaths: " + str(deaths) + " (" + unquote(riotid) + ")")
            #  If it does not exist or is private
            elif status == '451':
                message = responseJSON['message']
                await ctx.message.reply(message)
            elif status == '404':
                message = responseJSON['message']
                await ctx.message.reply(message)


def setup(bot):
    bot.add_cog(Valorant(bot))
