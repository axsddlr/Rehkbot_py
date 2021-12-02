import random

import nextcord
from googletrans import Translator
from nextcord.ext import commands


class FunCog(commands.Cog, name="Games & Fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll_dice", help="Simulates rolling dice.")
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(",".join(dice))

    @commands.command(aliases=["8ball"])
    async def eightball(self, ctx, *, arg):
        answers = [
            "As I see it, yes.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don’t count on it.",
            "It is certain.",
            "It is decidedly so.",
            "Most likely.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Outlook good.",
            "Reply hazy, try again.",
            "Signs point to yes.",
            "Very doubtful.",
            "Without a doubt.",
            "Yes.",
            "Yes – definitely.",
            "You may rely on it.",
        ]
        response = f"Question: {arg}\nAnswer: {random.choice(answers)}"
        await ctx.send(response)

    @commands.command(aliases=["flip", "coin"])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ["Heads", "Tails"]
        await ctx.send(
            f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!"
        )

    @commands.command(
        aliases=["pfp"],
        name="Avatar",
        help="Get the avatar URL of the tagged user(s), or your own avatar",
    )
    async def avatar(self, ctx):
        embed = nextcord.Embed(title=f"{ctx.author.name}'s avatar", color=0xDC143C)
        embed.set_image(url=ctx.author.avatar)
        embed.set_footer(text=f'Requested by {ctx.author}')

        await ctx.send(embed=embed)

    @commands.command(aliases=["translate"],
                      name="google translate",
                      help="Usage: `.translate {destination language} {the sentence you want to translate}",
                      )
    async def translate(self, ctx, lang, *, args):
        """Usage: `.translate {destination language} {the sentence you want to translate}`"""
        translator = Translator()
        translation = translator.translate(args, dest=lang)

        await ctx.send(f"{lang} " + "translation: " + f"**`{translation.text}`**")


def setup(bot):
    bot.add_cog(FunCog(bot))
