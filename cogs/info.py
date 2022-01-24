import datetime
import os
import time

import discord
import psutil
from discord.commands import slash_command
from discord.ext import commands

from utils.utils import cfg

guilds = [cfg["GUILD_ID"]]

start_time = time.time()


class InfoCog(commands.Cog, name="Info"):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.Cog.listener()
    async def on_ready(self):
        time.sleep(0.2)

    @slash_command(name="ping", description='Check bot latency.', guild_ids=guilds)
    async def ping(self, ctx):
        embed = discord.Embed(
            title='🏓|Pong!',
            description=f'Latency: {self.bot.latency} ms',
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)

    @slash_command(name="info", guild_ids=guilds)
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        ramUsage = self.process.memory_full_info().rss / 1024 ** 2
        avgmembers = round(len(self.bot.users) / len(self.bot.guilds))

        embed = discord.Embed(
            # crimson color code
            colour=0xDC143C
        )
        embed.set_thumbnail(url=ctx.author.avatar)
        embed.add_field(name="Uptime", value=text, inline=True)
        embed.add_field(name="Library", value="discord", inline=True)
        embed.add_field(
            name="Servers",
            value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers} users/server )",
            inline=True,
        )
        embed.add_field(
            name="# of Commands",
            value=len([x.name for x in self.bot.commands]),
            inline=True,
        )
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=True)

        await ctx.respond(content=f"ℹ About **{ctx.bot.user}** | **`1.0.0`**", embed=embed)

    @slash_command(name="members", guild_ids=guilds)
    async def membercount(self, ctx):
        embed = discord.Embed(title=ctx.guild.name, description=f"Members: {ctx.guild.member_count}",
                              color=0xDC143C)
        embed.set_footer(text=f"Requested by {ctx.author}")

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(InfoCog(bot))
