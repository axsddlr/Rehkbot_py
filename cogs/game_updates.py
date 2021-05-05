import discord
import requests
import os
import ujson as json
import time
import re
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from utils.discord_webhook import Webhook, Embed
from utils.functions import exists

load_dotenv()
patches_webhook = os.getenv("patches_webhook_url")
crimson = 0xDC143C


def getValorantGameUpdates():
    URL = "https://api.rehkloos.com/valorant/news/en-us/game-updates"
    response = requests.get(URL)
    return response.json()


def getLOLGameUpdates():
    URL = "https://api.rehkloos.com/lol/patch_notes"
    response = requests.get(URL)
    return response.json()


def getTFTGameUpdates():
    URL = "https://api.rehkloos.com/tft/patch_notes"
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
        banner = responseJSON["data"]["segments"]["thumbnail_url"]
        title = responseJSON["data"]["segments"]["title"]
        description = responseJSON["data"]["segments"]["description"]
        url = responseJSON["data"]["segments"]["url_path"]
        external_link = responseJSON["data"]["segments"]["external_link"]

        if external_link == "":
            full_url = "https://playvalorant.com/en-us" + url
        else:
            full_url = external_link

        # check if file exists
        exists(saved_json)

        time.sleep(5)

        # open saved_json file
        f = open(
            saved_json,
        )
        data = json.load(f)
        res = updater(data, "", None)
        check_file_json = res["data"]["segments"]["title"]

        # compare title string from file to title string from api then overwrite file
        if check_file_json == title:
            # print("True")
            return
        elif check_file_json != title:
            # print("False")
            hook = Webhook(patches_webhook)
            # hook.send(full_url)
            # f = open(saved_json, "w")
            # print(json.dumps(responseJSON), file=f)

            embed = Embed(
                title="VALORANT",
                description=f"[{title}]({full_url})\n\n{description}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Rehkbot")
            embed.set_image(url=banner)

            hook.send(embed=embed)

            f = open(saved_json, "w")
            print(json.dumps(responseJSON), file=f)

        f.close()

    async def lolupdates(self):
        await self.bot.wait_until_ready()

        # patch-notes channel
        saved_json = "lol_patch_old.json"
        responseJSON = getLOLGameUpdates()

        # JSON Results Mapping
        banner = responseJSON["data"]["segments"][0]["thumbnail"]
        title = responseJSON["data"]["segments"][0]["title"]
        url = responseJSON["data"]["segments"][0]["url"]

        # check if file exists
        exists(saved_json)

        time.sleep(5)

        # open saved_json file
        f = open(
            saved_json,
        )
        data = json.load(f)
        res = updater(data, "", None)
        check_file_json = res["data"]["segments"][0]["title"]

        # compare title string from file to title string from api then overwrite file
        if check_file_json == title:
            # print("True")
            return
        elif check_file_json != title:
            # print("False")
            hook = Webhook(patches_webhook)

            embed = Embed(
                title=title,
                description=url,
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Rehkbot")

            embed.set_image(url=banner)

            hook.send(embed=embed)

            f = open(saved_json, "w")
            print(json.dumps(responseJSON), file=f)

        f.close()

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.valupdates, "interval", seconds=3600)
        scheduler.add_job(self.lolupdates, "interval", seconds=3700)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(Game_Updates(bot))
