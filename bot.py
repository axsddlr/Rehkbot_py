import discord
from discord.ext import commands
import os

import sys
import traceback
from dotenv import load_dotenv

load_dotenv()


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


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = [
    'cogs.music',
    'cogs.badwords',
    'cogs.valorant',
    'cogs.commands']

bot = commands.Bot(command_prefix=get_prefix,
                   description='A Rewrite Cog Example')

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    # Twitch URL
    my_twitch_url = "https://twitch.tv/rehkloos"
    await bot.change_presence(activity=discord.Streaming(name="Rehkloos", url=my_twitch_url))
    print('Bot connected.')


bot.run(os.environ['DISCORD_TOKEN'], bot=True, reconnect=True)
