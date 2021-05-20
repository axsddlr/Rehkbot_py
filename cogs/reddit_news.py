import os
import time
import requests
import ujson as json
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands
from utils.discord_webhook import Webhook, Embed, File
from utils.global_utils import exists

load_dotenv()
reddit_webhook = os.getenv("reddit_webhook_url")
crimson = 0xDC143C


def getVALREDUpdates():
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }
    URL = "https://api.rehkloos.com/reddit/Valorant"
    response = requests.get(URL, headers=headers)
    return response.json()


def updater(d, inval, outval):
    for k, v in d.items():
        if isinstance(v, dict):
            updater(d[k], inval, outval)
        else:
            if v == "":
                d[k] = None
    return d


class Reddit_News(commands.Cog, name="Reddit News"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 900})

    async def reddit_monitor(self):
        await self.bot.wait_until_ready()

        # call API
        # patch-notes channel
        saved_json = "reddit_old.json"
        responseJSON = getVALREDUpdates()

        basetree = responseJSON["data"]["segments"][0]

        title = basetree["title"]
        thumbnail = basetree["thumbnail_url"]
        url_path = basetree["url_path"]
        author = basetree["author"]
        # description = basetree["selftext"]
        flair = basetree["flair"]
        full_url = "https://www.reddit.com" + url_path

        # check if file exists
        exists(saved_json)

        time.sleep(5)
        # open saved_json and check title string
        f = open(
            saved_json,
        )
        data = json.load(f)
        res = updater(data, "", None)
        check_file_json = res["data"]["segments"][0]["title"]

        if (flair != "Educational") and (check_file_json == title):
            # print("not patch notes")
            return
        elif (flair == "Educational") and (check_file_json != title):
            # print("False")
            hook = Webhook(reddit_webhook)

            embed = Embed(
                title="VALORANT REDDIT",
                description=f"[{title}]({full_url})\n\n author: {author}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Rehkbot")
            embed.set_image(url=thumbnail)
            file = File("./assets/images/val_reddit.png", name="val_reddit.png")
            embed.set_thumbnail(url="attachment://val_reddit.png")

            hook.send(embed=embed, file=file)
            f = open(saved_json, "w")
            print(json.dumps(responseJSON), file=f)

        f.close()

    @commands.Cog.listener()
    async def on_ready(self):

        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.reddit_monitor, "interval", seconds=900)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(Reddit_News(bot))
