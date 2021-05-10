import os
import requests
import ujson as json
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands
from utils.discord_webhook import Webhook, Embed

load_dotenv()
reddit_webhook = os.getenv("reddit_webhook_url")


def getVALREDUpdates():
    URL = "https://www.reddit.com/r/Valorant/new/.json"
    response = requests.get(URL)
    return response.json()


class Reddit_News(commands.Cog, name="Reddit News"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 900})

    async def reddit_monitor(self):
        await self.bot.wait_until_ready()

        # call API
        responseJSON = getVALREDUpdates()

        basetree = responseJSON["data"]["children"][0]["data"]

        title = basetree["title"]
        subreddit = basetree["subreddit"]
        thumbnail = basetree["thumbnail"]
        url_path = basetree["permalink"]
        # video = basetree["secure_media"]["reddit_video"]["fallback_url"]
        video_url = basetree["url"]
        author = basetree["author"]
        # description = basetree["selftext"]
        flair = basetree["link_flair_text"]
        full_url = "https://www.reddit.com" + url

        if flair != "Educational":
            # print("not patch notes")
            return
        elif flair == "Educational":
            # print("False")
            hook = Webhook(reddit_webhook)

            embed = Embed(
                title="VALORANT REDDIT",
                description=f"[{title}]({url})\n\n{author}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Rehkbot")
            embed.set_image(url=thumbnail)
            file = File("./assets/images/val_reddit.png", name="val_reddit.png")
            embed.set_thumbnail(url="attachment://val_reddit.png")

            hook.send(embed=embed, file=file)

    @commands.Cog.listener()
    async def on_ready(self):

        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.reddit_monitor, "interval", seconds=1800)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(Reddit_News(bot))
