import random

import discord
from discord.commands import slash_command
from discord.ext import commands
from googletrans import Translator
from discord import Option

from utils.utils import cfg

guilds = [cfg["GUILD_ID"]]


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

    @slash_command(
        name="pfp",
        description="Get the avatar URL of the tagged user(s), or your own avatar",
        guild_ids=guilds
    )
    async def avatar(self, ctx):
        embed = discord.Embed(title=f"{ctx.author.name}'s avatar", color=0xDC143C)
        embed.set_image(url=ctx.author.avatar)
        embed.set_footer(text=f'Requested by {ctx.author}')

        await ctx.respond(embed=embed)

    @slash_command(name="translate",
                   description="Usage: `.translate {destination language} {the sentence you want to translate}",
                   guild_ids=guilds)
    async def translate(self, ctx, lang, *, args):
        """Usage: `.translate {destination language} {the sentence you want to translate}`"""
        translator = Translator()
        translation = translator.translate(args, dest=lang)

        await ctx.respond(f"{lang} " + "translation: " + f"**`{translation.text}`**")

    @slash_command(name="rps", description="rock paper scissors", guild_ids=guilds)
    async def rps(self, ctx, rps: Option(str, "Rock Paper or Scissors", required=True, choices=["Rock", "Paper", "Scissors"])):
        choices = ["rock", "paper", "scissors"]
        cpu_choice = random.choice(choices)
        em = discord.Embed(title="Rock Paper Scissors")
        rps = rps.lower()
        if rps == 'rock':
            if cpu_choice == 'rock':
                em.description = "It's a tie!"
            elif cpu_choice == 'scissors':
                em.description = "You win!"
            elif cpu_choice == 'paper':
                em.description = "You lose!"

        elif rps == 'paper':
            if cpu_choice == 'paper':
                em.description = "It's a tie!"
            elif cpu_choice == 'rock':
                em.description = "You win!"
            elif cpu_choice == 'scissors':
                em.description = "You lose!"

        elif rps == 'scissors':
            if cpu_choice == 'scissors':
                em.description = "It's a tie!"
            elif cpu_choice == 'paper':
                em.description = "You win!"
            elif cpu_choice == 'rock':
                em.description = "You lose!"

        else:
            em.description = "Invalid Input"

        em.add_field(name="Your Choice", value=rps)
        em.add_field(name="Bot Choice", value=cpu_choice)
        await ctx.respond(embed=em)


def setup(bot):
    bot.add_cog(FunCog(bot))
