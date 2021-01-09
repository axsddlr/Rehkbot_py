import discord
import random
import time
from discord.ext import commands


class GamesCog(commands.Cog, name='GamesN'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll_dice', help='Simulates rolling dice.')
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        dice = [str(random.choice(range(1, number_of_sides + 1)))
                for _ in range(number_of_dice)
                ]
        await ctx.send(','.join(dice))

    @commands.command(aliases=['8ball'])
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
            "You may rely on it."
        ]
        response = f"Question: {arg}\nAnswer: {random.choice(answers)}"
        await ctx.send(response)

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.


def setup(bot):
    bot.add_cog(GamesCog(bot))
