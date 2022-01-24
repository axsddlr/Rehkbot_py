from better_profanity import profanity
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
from discord.commands import slash_command
from utils.utils import cfg

guilds = [cfg["GUILD_ID"]]

profanity.load_censor_words_from_file("./assets/bad_words.txt")


class Profanity(Cog, name="Profanity"):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="addprofanity", guild_ids=guilds)
    @has_permissions(manage_guild=True)
    async def add_profanity(self, ctx, *words):
        with open("./assets/bad_words.txt", "a", encoding="utf-8") as f:
            f.write("".join([f"{w}\n" for w in words]))

        profanity.load_censor_words_from_file("./assets/bad_words.txt")
        await ctx.respond("Action complete.")

    @slash_command(name="delprofanity", guild_ids=guilds)
    @has_permissions(manage_guild=True)
    async def remove_profanity(self, ctx, *words):
        with open("./assets/bad_words.txt", "r", encoding="utf-8") as f:
            stored = [w.strip() for w in f.readlines()]

        with open("./assets/bad_words.txt", "w", encoding="utf-8") as f:
            f.write("".join([f"{w}\n" for w in stored if w not in words]))

        profanity.load_censor_words_from_file("./assets/bad_words.txt")
        await ctx.respond("Action complete.")

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if profanity.contains_profanity(message.content):
                await message.delete()
                await message.channel.send("You can't use that word here.")


def setup(bot):
    bot.add_cog(Profanity(bot))
