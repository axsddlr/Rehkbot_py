import discord
import requests
import os
import ujson as json
import time
import sys
import traceback
from discord.ext import commands
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
STREAMER_NAME = os.getenv("STREAMER")

scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 900})


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ["!"]

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return "?"

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix, description="A Rewrite Cog Example")
bot.remove_command("help")


# This is what we're going to use to load the cogs on startup
if __name__ == "__main__":
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


initial_ext = ["cogs.twitchlive"]


async def reload():
    for extension in initial_ext:
        try:
            # bot.unload_extension(extension)
            # bot.load_extension(extension)
            bot.reload_extension(extension)
            print("done")
        except Exception as e:
            print(f"Failed to load the {extension}", file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    # Twitch URL
    my_twitch_url = "https://twitch.tv/" + f"{STREAMER_NAME}"
    await bot.change_presence(
        activity=discord.Streaming(name="Rehhk", url=my_twitch_url)
    )
    print("Bot connected")

    scheduler.add_job(
        reload, CronTrigger(day_of_week="mon-sun", hour="21", timezone="US/Eastern")
    )
    # scheduler.add_job(reload, "interval", seconds=43200)

    # starting the scheduler
    scheduler.start()


bot.run(TOKEN, bot=True, reconnect=True)
