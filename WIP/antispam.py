from discord.ext import commands
from AntiSpam import AntiSpamHandler

warn_embed_dict = {
    "title": "**Dear $USERNAME**",
    "description": "You are being warned for spam, please stop!",
    "timestamp": True,
    "color": 0xFF0000,
    "footer": {"text": "$BOTNAME", "icon_url": "$BOTAVATAR"},
    "author": {"name": "$GUILDNAME", "icon_url": "$GUILDICON"},
    "fields": [
        {"name": "Current warns:", "value": "$WARNCOUNT", "inline": False},
        {"name": "Current kicks:", "value": "$KICKCOUNT", "inline": False},
    ],
}

class AntiSpamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.handler = AntiSpamHandler(self.bot, guild_warn_message=warn_embed_dict)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.handler.propagate(message)

def setup(bot):
    bot.add_cog(AntiSpamCog(bot))
