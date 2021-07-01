from re import search
from discord.ext.commands import Cog


class Links(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.links_allowed = (
            817593711054815252,
            512694755847831562,
            512698020484087812,
            824453152526565427,
            859701236714700810,
            857484003086827521,
        )
        self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.channel.id not in self.links_allowed:
                if search(self.url_regex, message.content):
                    await message.delete()
                    await message.channel.send(
                        "No links allowed in this channel!", delete_after=10
                    )
                else:
                    return


def setup(bot):
    bot.add_cog(Links(bot))
