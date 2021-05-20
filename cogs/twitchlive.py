import os
import requests
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands
from utils.discord_webhook import Webhook, Embed

load_dotenv()
twitch_webhook = os.getenv("twitch_live_url")
TCI = os.getenv("TWITCH_CLIENT_ID")
TCS = os.getenv("TWITCH_CLIENT_SECRET")
STREAMER_NAME = os.getenv("STREAMER")
crimson = 0xDC143C

URL = "https://api.twitch.tv/helix/streams?user_login=" + f"{STREAMER_NAME}"
authURL = "https://id.twitch.tv/oauth2/token"
GAME_URL = "https://api.twitch.tv/helix/games?id="

AutParams = {"client_id": TCI, "client_secret": TCS, "grant_type": "client_credentials"}


def twitch_request():
    AutCall = requests.post(url=authURL, params=AutParams)
    access_token = AutCall.json()["access_token"]

    head = {"Client-ID": TCI, "Authorization": "Bearer " + access_token}

    response = requests.get(URL, headers=head)
    return response.json()


class TwitchLive(commands.Cog, name="Twitch Live"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 210})

    async def is_live(self):
        await self.bot.wait_until_ready()

        # call regular twitch api
        responseJSON = twitch_request()

        if len(responseJSON["data"]) == 1:
            print("live")
            hook = Webhook(twitch_webhook)

            title = responseJSON["data"][0]["title"]
            stream_url = "https://twitch.tv/" + f"{STREAMER_NAME}"
            game_id = responseJSON["data"][0]["game_id"]
            # call twitch game api then combine game_id from regular twitch api
            GameJSON = GAME_URL + game_id

            # request twitch game data
            AutCall = requests.post(url=authURL, params=AutParams)
            access_token = AutCall.json()["access_token"]
            head = {"Client-ID": TCI, "Authorization": "Bearer " + access_token}
            response = requests.get(GameJSON, headers=head)
            GJSON = response.json()

            # api elements from twitch game api
            game_name = GJSON["data"][0]["name"]
            game_art = GJSON["data"][0]["box_art_url"].format(width="340", height="452")

            embed = Embed(
                title=title,
                description=stream_url,
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Rehkbot")

            embed.set_image(url=game_art)

            hook.send(
                ":mega: live now, playing VALORANT! @everyone",
                embed=embed,
            )

            self.scheduler.pause()
        else:
            self.scheduler.resume()

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.is_live, "interval", seconds=420, id="live")
        scheduler.get_job(
            "live", CronTrigger(day_of_week="mon-sun", hour="21", timezone="US/Eastern")
        ).resume()

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(TwitchLive(bot))
