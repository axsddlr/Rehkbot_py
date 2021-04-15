import discord
import requests
import os
import ujson as json
import time
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from utils.discord_webhook import Webhook, Embed

load_dotenv()
spike_webhook = os.getenv("spike_webhook_url")


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


class Game_News(commands.Cog, name="Game News"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 900})

    async def spike_monitor(self):
        await self.bot.wait_until_ready()

        saved_json = "spike_old.json"
        # call API
        responseJSON = getSpikeUpdates()

        title = responseJSON["today"][0]["title"]
        url = responseJSON["today"][0]["url_path"]
        full_url = "https://thespike.gg" + url

        time.sleep(5)
        # open saved_json and check title string
        f = open(
            saved_json,
        )
        data = json.load(f)
        res = updater(data, "", None)
        check_file_json = res["today"][0]["title"]

        # compare title string from file to title string from api then overwrite file
        if check_file_json == title:
            # print("True")
            return
        elif check_file_json != title:
            # print("False")
            hook = Webhook(spike_webhook)
            hook.send(full_url)
            f = open(saved_json, "w")
            print(json.dumps(responseJSON), file=f)

        f.close()

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.spike_monitor, "interval", seconds=1800)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(Game_News(bot))
