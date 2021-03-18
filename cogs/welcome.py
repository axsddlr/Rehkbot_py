import discord
import time
import sys
import psutil
import os
import datetime
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Cog

load_dotenv()
WELCOME_CHANNEL_ID = os.getenv('WELCOME')
LEAVE_CHANNEL_ID = os.getenv('WELCOME')

class Streaming(Cog, name='Streaming'):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        try:
            channel = bot.get_channel(WELCOME_CHANNEL_ID)
            try:
                embed = discord.Embed(colour=discord.Colour.green())
                embed.set_author(name=member.name, icon_url=member.avatar_url)
                embed.add_field(name="Welcome", value=f"**Hey,{member.mention}! Welcome to {member.guild.name}\nI hope you enjoy your stay here!\nThanks for joining**", inline=False)
                embed.set_thumbnail(url=member.guild.icon_url)
                await channel.send(embed=embed)
            except Exception as e:
                raise e
        except Exception as e:
            raise e

    @Cog.listener()
    async def on_member_remove(self, member):
        try:
            channel = bot.get_channel(LEAVE_CHANNEL_ID)
            try:
                embed = discord.Embed(colour=discord.Colour.red())
                embed.set_author(name=member.name, icon_url=member.avatar_url)
                embed.add_field(name="Good Bye", value=f"**{member.mention} just left us.**", inline=False)
                embed.set_thumbnail(url=member.guild.icon_url)
                await channel.send(embed=embed)
            except Exception as e:
                raise e
        except Exception as e:
            raise e

def setup(bot):
    	bot.add_cog(Streaming(bot))
