import discord
import sys
import os
from discord.ext import commands


# automatic moderation
f1 = open('./assets/bad_words.txt', 'r')
bw = f1.readlines()

bad_words = []
for i in range(len(bw)):
    bad_words.append(bw[i].replace("\n", ""))


class BadwordsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        # No infinite bot loops
        if msg.author.bot:
            return
        for word in bad_words:
            if word in msg.content.lower():
                await msg.delete()
                mention = msg.author.mention
                await msg.channel.send(f"{ mention } THAT WORD IS NOT PERMITTED!")

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.


# close all open files
f1.close()


def setup(bot):
    bot.add_cog(BadwordsCog(bot))
