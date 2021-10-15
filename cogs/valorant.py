import nextcord
import requests
from nextcord.ext import commands
from nextcord.ext.commands.cooldowns import BucketType


def getValorantGameUpdates():
    URL = "https://api.henrikdev.xyz/valorant/v1/website/en-us?filter=game_updates"
    response = requests.get(URL)
    return response.json()


def getValorantRank(Region, Name, Tag):
    URL = "https://api.henrikdev.xyz/valorant/v1/mmr/" + Region + "/" + Name + "/" + Tag
    response = requests.get(URL)
    return response.json()


def getValorantLevel(Name, Tag):
    URL = "https://api.henrikdev.xyz/valorant/v1/account/" + Name + "/" + Tag
    response = requests.get(URL)
    return response.json()


def getValorantStats(Name, Tag, Type):
    URL = "http://vlrscrape.herokuapp.com/v1/stats/" + Name + "/" + Tag + "/" + Type
    response = requests.get(URL)
    return response.json()


class Valorant(commands.Cog, name="Valorant"):
    def __init__(self, bot):
        self.bot = bot

    #  Valorant News
    @commands.command(
        name="Valorant News",
        aliases=["valupdates"],
        help="Displays Valorant Latest Patches",
    )
    @commands.cooldown(2, 60, BucketType.user)
    async def valupdates(self, ctx):

        banner = ""
        title = ""
        url = ""
        responseJSON = getValorantGameUpdates()

        # JSON Results Mapping
        banner = responseJSON["data"][0]["banner_url"]
        title = responseJSON["data"][0]["title"]
        url = responseJSON["data"][0]["url"]

        embed = nextcord.Embed(
            title=title,
            description=url,
            # crimson color code
            colour=0xDC143C,
        )
        embed.set_image(url=banner)
        file = nextcord.File(
            "./assets/images/valorant_sm.png", filename="valorant_sm.png"
        )
        embed.set_thumbnail(url="attachment://valorant_sm.png")

        await ctx.send(file=file, embed=embed)

    @commands.command(
        name="Valorant Rank", aliases=["valrank"], help="Displays Valorant Rank"
    )
    # @commands.cooldown(2, 60, BucketType.user)
    async def valrank(self, ctx, Region, Name, Tag):

        responseJSON = getValorantRank(Region, Name, Tag)
        responseJSON2 = getValorantLevel(Name, Tag)

        # Check if profile exists or is public
        status = responseJSON["status"]
        if status == "200":
            riotid = Name + "#" + Tag
            rank = responseJSON["data"]["currenttierpatched"]
            elo = responseJSON["data"]["elo"]
            level = responseJSON2["data"]["account_level"]

            await ctx.message.reply("Rank: " + str(rank) + " | " + "Elo: " + str(elo) + " | " + "Level: " + str(level))
            #  If it does not exist or is private
        elif status == "451":
            message = responseJSON["message"]
            await ctx.message.reply(message)
        elif status == "404":
            message = responseJSON["message"]
            await ctx.message.reply(message)
        elif status == "459":
            message = responseJSON["message"]
            await message.reply(message)

    @commands.command(
        name="Valorant Stats",
        aliases=["valstats"],
        help="Displays General Valorant Stats",
    )
    # @commands.cooldown(2, 60, BucketType.user)
    async def valstats(self, ctx, Name: str = "", Tag: str = "", Type: str = ""):

        responseJSON = getValorantStats(Name, Tag, Type)

        # Check if profile exists or is public
        # status = responseJSON['status']
        # if status == '200':
        riotid = Name + "#" + Tag
        kills = responseJSON["data"]["segments"]["kills"]
        deaths = responseJSON["data"]["segments"]["deaths"]
        kdr = responseJSON["data"]["segments"]["kd"]
        wins = responseJSON["data"]["segments"]["wins"]
        winr = responseJSON["data"]["segments"]["win_percentage"]
        # TTP = responseJSON['data']['segments']['playtime']['playtimepatched']
        asst = responseJSON["data"]["segments"]["assists"]
        # matches = responseJSON['data']['segments']['matches']
        headshots = responseJSON["data"]["segments"]["headshots"]
        headshotpercentage = responseJSON["data"]["segments"]["headshot_percentage"]
        firstbloods = responseJSON["data"]["segments"]["firstBlood"]
        aces = responseJSON["data"]["segments"]["ace"]
        clutches = responseJSON["data"]["segments"]["clutch"]
        flawless = responseJSON["data"]["segments"]["flawless"]
        # user = responseJSON['user']
        url = (
                "https://tracker.gg/valorant/profile/riot/"
                + Name
                + "%23"
                + Tag
                + "/overview?playlist="
                + Type
        )

        embed = nextcord.Embed(
            title=riotid + "'s " + Type,
            description=url,
            # crimson color code
            colour=0xDC143C,
        )
        file = nextcord.File(
            "./assets/images/valorant_sm.png", filename="valorant_sm.png"
        )
        embed.set_thumbnail(url="attachment://valorant_sm.png")
        # embed.add_field(name="Total Time Played", value=(TTP), inline=True)
        embed.add_field(name="Kills", value=kills, inline=True)
        embed.add_field(name="Deaths", value=deaths, inline=True)
        embed.add_field(name="Wins", value=wins, inline=True)
        embed.add_field(name="Win %", value=winr, inline=True)
        embed.add_field(name="KDR", value=kdr, inline=True)
        embed.add_field(name="Assists", value=asst, inline=True)
        # embed.add_field(name="Matches", value=(matches), inline=True)
        embed.add_field(name="Headshots", value=headshots, inline=True)
        embed.add_field(name="Headshots %", value=headshotpercentage, inline=True)
        embed.add_field(name="First Bloods", value=firstbloods, inline=True)
        embed.add_field(name="Aces", value=aces, inline=True)
        embed.add_field(name="Clutches", value=clutches, inline=True)
        embed.add_field(name="Flawless", value=flawless, inline=True)
        embed.add_field(name=" .", value=". ", inline=True)

        await ctx.send(file=file, embed=embed)

        # #  If it does not exist or is private
        # elif status == '451':
        #     message = responseJSON['message']
        #     await ctx.message.reply(message)
        # elif status == '404':
        #     message = responseJSON['message']
        #     await ctx.message.reply(message)
        # elif status == '459':
        #     message = responseJSON['message']
        #     await message.reply(message)


def setup(bot):
    bot.add_cog(Valorant(bot))
