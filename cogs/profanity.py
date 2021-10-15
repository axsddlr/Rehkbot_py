from better_profanity import profanity
from nextcord.ext.commands import Cog
from nextcord.ext.commands import command, has_permissions

profanity.load_censor_words_from_file("./assets/bad_words.txt")


class Profanity(Cog, name="Profanity"):
    def __init__(self, bot):
        self.bot = bot

    @command(name="addprofanity", aliases=["addswears", "addcurses"])
    @has_permissions(manage_guild=True)
    async def add_profanity(self, ctx, *words):
        with open("./assets/bad_words.txt", "a", encoding="utf-8") as f:
            f.write("".join([f"{w}\n" for w in words]))

        profanity.load_censor_words_from_file("./assets/bad_words.txt")
        await ctx.send("Action complete.")

    @command(name="delprofanity", aliases=["delswears", "delcurses"])
    @has_permissions(manage_guild=True)
    async def remove_profanity(self, ctx, *words):
        with open("./assets/bad_words.txt", "r", encoding="utf-8") as f:
            stored = [w.strip() for w in f.readlines()]

        with open("./assets/bad_words.txt", "w", encoding="utf-8") as f:
            f.write("".join([f"{w}\n" for w in stored if w not in words]))

        profanity.load_censor_words_from_file("./assets/bad_words.txt")
        await ctx.send("Action complete.")

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if profanity.contains_profanity(message.content):
                await message.delete()
                await message.channel.send("You can't use that word here.")


def setup(bot):
    bot.add_cog(Profanity(bot))
