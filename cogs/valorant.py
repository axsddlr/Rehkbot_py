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


def getValorantRank(Region, Name, Tag):
    URL = "https://api.henrikdev.xyz/valorant/v1/mmr/" + Region + "/" + Name + "/" + Tag
    response = requests.get(URL)
    return response.json()


def getValorantStats(Name, Tag):
    URL = "https://api.henrikdev.xyz/valorant/v1/profile/" + Name + "/" + Tag
    response = requests.get(URL)
    return response.json()

class Valorant(commands.Cog, name='Valorant'):
    def __init__(self, bot):
        self.bot = bot

    #  Valorant News
    @commands.command(name='Valorant News',
                      aliases=['valupdates'],
                      help='Displays Valorant Latest Patches')
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

    @commands.command(name='Valorant Rank',
                      aliases=['valrank'],
                      help='Displays Valorant Rank')
    # @commands.cooldown(2, 60, BucketType.user)
    async def valrank(self, ctx, Region: str = "", Name: str = "", Tag: str = ""):

        responseJSON = getValorantRank(Region, Name, Tag)

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

    @commands.command(name='Valorant Stats',
                      aliases=['valstats'],
                      help='Displays General Valorant Stats')
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
                asst = responseJSON['stats']['assists']
                matches = responseJSON['stats']['matches']
                headshots = responseJSON['stats']['headshots']
                headshotpercentage = responseJSON['stats']['headshotpercentage']
                firstbloods = responseJSON['stats']['firstbloods']
                aces = responseJSON['stats']['aces']
                clutches = responseJSON['stats']['clutches']
                flawless = responseJSON['stats']['flawless']
                user = responseJSON['user']
                url = "https://tracker.gg/valorant/profile/riot/" + Name + "%23" + Tag + "/overview"

                embed = discord.Embed(
                    title=user + "'s Stats",
                    description=url,
                    # crimson color code
                    colour=(0xDC143C)
                )
                file = discord.File("./assets/images/hex_valorant_logo.png", filename="hex_valorant_logo.png")
                embed.set_thumbnail(url="attachment://hex_valorant_logo.png")
                embed.add_field(name="Total Time Played", value=(TTP), inline=True)
                embed.add_field(name=('Kills'), value=(kills), inline=True)
                embed.add_field(name=("Deaths"), value=(deaths), inline=True)
                embed.add_field(name="Wins", value=(wins), inline=True)
                embed.add_field(name="Win %", value=(winr), inline=True)
                embed.add_field(name="KDR", value=(kdr), inline=True)
                embed.add_field(name="Assists", value=(asst), inline=True)
                embed.add_field(name="Matches", value=(matches), inline=True)
                embed.add_field(name="Headshots", value=(headshots), inline=True)
                embed.add_field(name="Headshots %", value=(headshotpercentage), inline=True)
                embed.add_field(name="First Bloods", value=(firstbloods), inline=True)
                embed.add_field(name="Aces", value=(aces), inline=True)
                embed.add_field(name="Clutches", value=(clutches), inline=True)
                embed.add_field(name="Flawless", value=(flawless), inline=True)
                embed.add_field(name=" .", value=(". "), inline=True)

                await ctx.send(file=file, embed=embed)


            #  If it does not exist or is private
            elif status == '451':
                message = responseJSON['message']
                await ctx.message.reply(message)
            elif status == '404':
                message = responseJSON['message']
                await ctx.message.reply(message)


def setup(bot):
    bot.add_cog(Valorant(bot))
