import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
STREAMER_NAME = os.getenv("STREAMER")


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ["!"]

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return "?"

    # allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix, description="A Rewrite Cog Example")
bot.remove_command("help")


# This is what we're going to use to load the cogs on startup
if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            try:
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
    await bot.change_presence(
        activity=discord.Streaming(name="Rehhk", url=my_twitch_url)
    )
    print("Bot connected")


bot.run(TOKEN, reconnect=True)
