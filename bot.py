import discord
import requests
from discord.ext import commands
import os

import sys
import traceback
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)

def getValorantGameUpdates():
    URL = "https://api.henrikdev.xyz/valorant/v1/website/en-us?filter=game_updates"
    response = requests.get(URL)
    return response.json()

async def valupdates():
    await bot.wait_until_ready()

    # patch-notes channel
    c = bot.get_channel(512698020484087812)


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
    file = discord.File("./assets/images/valorant_sm.png", filename="valorant_sm.png")
    embed.set_thumbnail(url="attachment://valorant_sm.png")

    await c.send(file=file, embed=embed)




bot = commands.Bot(command_prefix=get_prefix,
                   description='A Rewrite Cog Example')
bot.remove_command('help')


# This is what we're going to use to load the cogs on startup
if __name__ == '__main__':
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):  # We only want to check through the python files
         try:  # I'd rather have this try/except block as I'd like it to load even if there is an issue with the cogs
            # This will load it
            bot.load_extension("cogs.{0}".format(filename[:-3]))
            # this is to let us know which cogs got loaded
            print("{0} is online".format(filename[:-3]))
         except:
            print("{0} was not loaded".format(filename))
            continue


@bot.event
async def on_ready():
    # Twitch URL
    my_twitch_url = "https://twitch.tv/rehkloos"
    await bot.change_presence(activity=discord.Streaming(name="Rehkloos", url=my_twitch_url))
    print('Bot connected.')
    # bot.load_extension("twitter_feed.twitterfeed")
    scheduler = AsyncIOScheduler()

    # checks for new patch every Tuesday at 1pm EST
    scheduler.add_job(valupdates, CronTrigger(day_of_week='tue', hour="13", timezone='US/Eastern'))

    #starting the scheduler
    scheduler.start()



bot.run(TOKEN, bot=True, reconnect=True)
