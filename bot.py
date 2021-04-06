import discord
import requests
import os
import sys
import traceback
import ujson as json
import time
from discord.ext import commands
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from utils.discord_webhook import Webhook, Embed

load_dotenv()
scheduler = AsyncIOScheduler(job_defaults={'misfire_grace_time': 900})


TOKEN = os.getenv('DISCORD_TOKEN')
spike_webhook = os.getenv('spike_webhook_url')
patches_webhook = os.getenv('patches_webhook_url')
TCI = os.getenv('TWITCH_CLIENT_ID')
TCS = os.getenv('TWITCH_CLIENT_SECRET')
STREAMER_NAME = os.getenv('STREAMER')

URL = 'https://api.twitch.tv/helix/streams?user_login=' + f"{STREAMER_NAME}"
authURL = 'https://id.twitch.tv/oauth2/token'

AutParams = {'client_id': TCI,
             'client_secret': TCS,
             'grant_type': 'client_credentials'
             }


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


def twitch_request():
    AutCall = requests.post(url=authURL, params=AutParams)
    access_token = AutCall.json()['access_token']

    head = {
        'Client-ID': TCI,
        'Authorization':  "Bearer " + access_token
    }

    response = requests.get(URL, headers=head)
    return response.json()


def getValorantGameUpdates():
    URL = "https://api.henrikdev.xyz/valorant/v1/website/en-us?filter=game_updates"
    response = requests.get(URL)
    return response.json()


def getSpikeUpdates():
    URL = "https://spikegg-scrape.herokuapp.com/latest_news"
    response = requests.get(URL)
    return response.json()


def updater(d, inval, outval):
    for k, v in d.items():
        if isinstance(v, dict):
            updater(d[k], inval, outval)
        else:
            if v == "":
                d[k] = None
    return d


async def spike_monitor():
    await bot.wait_until_ready()

    saved_json = "spike_old.json"
    # call API
    responseJSON = getSpikeUpdates()
    title = responseJSON['today'][0]['title']
    url = responseJSON['today'][0]['url_path']
    full_url = "https://thespike.gg" + url

    time.sleep(5)
    # open saved_json and check title string
    f = open(saved_json,)
    data = json.load(f)
    res = updater(data, "", None)
    check_file_json = res['today'][0]['title']

    #compare title string from file to title string from api then overwrite file
    if check_file_json == title:
        # print("True")
        return
    elif check_file_json != title:
        # print("False")
        #send to news channel in discord
        #c = bot.get_channel(824453152526565427)
        # JSON Results Mapping
        # await c.send(full_url)
        hook = Webhook(spike_webhook)
        hook.send(full_url)
        f = open(saved_json, "w")
        print(json.dumps(responseJSON), file=f)

    f.close()


async def valupdates():
    await bot.wait_until_ready()

    # patch-notes channel
    saved_json = "valo_patch_old.json"
    responseJSON = getValorantGameUpdates()

    # JSON Results Mapping
    banner = responseJSON['data'][0]['banner_url']
    title = responseJSON['data'][0]['title']
    url = responseJSON['data'][0]['url']

    #open saved_json file
    f = open(saved_json,)
    data = json.load(f)
    res = updater(data, "", None)
    check_file_json = res['data'][0]['title']

    #compare title string from file to title string from api then overwrite file
    if check_file_json == title:
        # print("True")
        return
    elif check_file_json != title:
        # print("False")
        #send to news channel in discord
        #c = bot.get_channel(824453152526565427)
        # JSON Results Mapping
        # await c.send(full_url)
        hook = Webhook(patches_webhook)
        hook.send(url)
        f = open(saved_json, "w")
        print(json.dumps(responseJSON), file=f)

    f.close()


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
    my_twitch_url = "https://twitch.tv/" + f"{STREAMER_NAME}"
    await bot.change_presence(activity=discord.Streaming(name="Rehhk", url=my_twitch_url))
    print('Bot connected')

    # checks for new patch every Tuesday at 1pm EST
    # scheduler.add_job(valupdates, CronTrigger(day_of_week='tue', hour="13", timezone='US/Eastern'))
    scheduler.add_job(valupdates, 'interval', seconds=3600)
    scheduler.add_job(spike_monitor, 'interval', seconds=1800)

    #starting the scheduler
    scheduler.start()


bot.run(TOKEN, bot=True, reconnect=True)
