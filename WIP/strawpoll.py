from discord.commands import slash_command
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from utils.utils import cfg

guilds = [cfg["GUILD_ID"]]


class StrawPoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def find_title(message):
        # this is the index of the first character of the title
        first = message.find("{") + 1
        # index of the last character of the title
        last = message.find("}")
        if first == 0 or last == -1:
            # TODO: Send a message telling the use how they are using it incorrectly.
            return "Not using the command correctly"
        return message[first:last]

    def find_options(self, message, options):
        # first index of the first character of the option
        first = message.find("[") + 1
        # index of the last character of the title
        last = message.find("]")
        if first == 0 or last == -1:
            if len(options) < 2:
                # TODO: Send a message telling the use how they are using it incorrectly.
                return "Not using the command correctly"
            else:
                return options
        options.append(message[first:last])
        message = message[last + 1:]
        return self.find_options(message, options)

    @slash_command(
        name="strawpoll",
        guild_ids=guilds,
    )
    @commands.cooldown(2, 60, BucketType.user)
    async def strawpoll(self, ctx):
        if not ctx.message.author.bot:
            message = ctx.message.clean_content

            title = self.find_title(message)

            options = self.find_options(message, [])

            try:
                async with self.bot.http_session.post(
                        "https://strawpoll.com/api/poll",
                        json={
                            "poll": {
                                "title": title,
                                "answers": options,
                            }
                        },
                        headers={"Content Type": "application/json"},
                ) as resp:
                    json = await resp.json()

                    await ctx.message.channel.respond(
                        "https://strawpoll.com/" + str(json["content_id"])
                    )

            except KeyError:
                return "Please make sure you are using the format '+strawpoll {title} [Option1] [Option2] [Option 3]'"

    @strawpoll.error
    async def strawpoll_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(error)


def setup(bot):
    bot.add_cog(StrawPoll(bot))
