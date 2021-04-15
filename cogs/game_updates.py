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
from utils.functions import exists

load_dotenv()
patches_webhook = os.getenv("patches_webhook_url")


def getValorantGameUpdates():
    URL = "https://api.henrikdev.xyz/valorant/v1/website/en-us?filter=game_updates"
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


class Game_Updates(commands.Cog, name="Game Updates"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 900})

    async def valupdates(self):
        await self.bot.wait_until_ready()

        # patch-notes channel
        saved_json = "valo_patch_old.json"
        responseJSON = getValorantGameUpdates()

        # JSON Results Mapping
        banner = responseJSON["data"][0]["banner_url"]
        title = responseJSON["data"][0]["title"]
        url = responseJSON["data"][0]["url"]

        # check if file exists
        exists(saved_json)

        time.sleep(5)

        # open saved_json file
        f = open(
            saved_json,
        )
        data = json.load(f)
        res = updater(data, "", None)
        check_file_json = res["data"][0]["title"]

        # compare title string from file to title string from api then overwrite file
        if check_file_json == title:
            # print("True")
            return
        elif check_file_json != title:
            # print("False")
            hook = Webhook(patches_webhook)
            hook.send(url)
            f = open(saved_json, "w")
            print(json.dumps(responseJSON), file=f)

        f.close()

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.valupdates, "interval", seconds=3600)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(Game_Updates(bot))
