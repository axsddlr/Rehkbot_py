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
from utils.discord_webhook import Webhook, Embed, File
from utils.global_utils import news_exists, matches_exists

load_dotenv()
spike_webhook = os.getenv("spike_webhook_url")
vlr_matches_webhook = os.getenv("vlr_matches_webhook_url")
crimson = 0xDC143C


def getSpikeUpdates():
    URL = "https://api.rehkloos.com/spikegg/latest_news"
    response = requests.get(URL)
    return response.json()


def getVLRUpdates():
    URL = "https://api.rehkloos.com/vlr/latest_news"
    response = requests.get(URL)
    return response.json()


def getVLRMatches():
    URL = "https://api.rehkloos.com/vlr/match/results"
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

        # check if file exists
        exists(saved_json)

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

    async def vlr_news_monitor(self):
        await self.bot.wait_until_ready()

        saved_json = "vlr_old.json"

        # call API
        responseJSON = getVLRUpdates()

        title = responseJSON["data"]["segments"][0]["title"]
        description = responseJSON["data"]["segments"][0]["description"]
        author = responseJSON["data"]["segments"][0]["author"]
        url = responseJSON["data"]["segments"][0]["url_path"]
        full_url = "https://www.vlr.gg" + url

        # check if file exists
        news_exists(saved_json)

        time.sleep(5)
        # open saved_json and check title string
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
            hook = Webhook(spike_webhook)
            hook.send(full_url)

            f = open(saved_json, "w")
            print(json.dumps(responseJSON), file=f)

        f.close()

    async def vlr_matches_monitor(self):
        await self.bot.wait_until_ready()

        saved_json = "./vlr_matches.json"

        # call API
        responseJSON = getVLRMatches()

        team1 = responseJSON["data"]["segments"][0]["team1"]
        team2 = responseJSON["data"]["segments"][0]["team2"]
        score1 = responseJSON["data"]["segments"][0]["score1"]
        score2 = responseJSON["data"]["segments"][0]["score2"]
        flag1 = responseJSON["data"]["segments"][0]["flag1"]
        flag2 = responseJSON["data"]["segments"][0]["flag2"]
        time_completed = responseJSON["data"]["segments"][0]["time_completed"]
        round_info = responseJSON["data"]["segments"][0]["round_info"]
        tournament_name = responseJSON["data"]["segments"][0]["tournament_name"]
        url = responseJSON["data"]["segments"][0]["match_page"]
        tournament_icon = responseJSON["data"]["segments"][0]["tournament_icon"]
        full_url = "https://www.vlr.gg" + url

        # check if file exists
        matches_exists(saved_json)

        time.sleep(5)
        # open saved_json and check title string
        f = open(
            saved_json,
        )
        data = json.load(f)
        res = updater(data, "", None)

        check_file_json = res["data"]["segments"][0]["team1"]

        # compare title string from file to title string from api then overwrite file
        if check_file_json == team1:
            # print("True")
            return
        elif check_file_json != team1:
            # print("False")
            hook = Webhook(vlr_matches_webhook)

            embed = Embed(
                title=f"**VLR Match Results**",
                description=f"**{tournament_name}**\n\n[Match page]({full_url})\n\n",
                color=crimson,
                # timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text=f"{round_info} | {time_completed}")
            embed.add_field(
                name=f"__Teams__",
                value=f":{flag1}: **{team1}**\n:{flag2}: **{team2}**",
                inline=True,
            )
            embed.add_field(
                name=f"__Result__", value=f"**{score1}**\n**{score2}**", inline=True
            )
            embed.set_thumbnail(url=f"{tournament_icon}")

            hook.send(embed=embed)

            f = open(saved_json, "w")
            print(json.dumps(responseJSON), file=f)

        f.close()

    @commands.Cog.listener()
    async def on_ready(self):

        scheduler = self.scheduler

        # add job for scheduler
        # scheduler.add_job(self.spike_monitor, "interval", seconds=1800)
        scheduler.add_job(self.vlr_matches_monitor, "interval", seconds=600)
        scheduler.add_job(self.vlr_news_monitor, "interval", seconds=1800)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(Game_News(bot))
