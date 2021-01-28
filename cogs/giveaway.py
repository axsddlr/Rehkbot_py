import discord
from discord.ext import commands
import random
import asyncio
import sqlite3

class Giveaway(commands.Cog):
    """
    Giveaway commands
    """
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect("./app.db")
        self.cr = self.db.cursor()

    @commands.command(
        name='gcreate',
        help='to made giveaway advanced settings')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def giveaway_create(self, ctx):
        questions = [
            "Which channel should it be hosted in?",
            "What should be the duration of the giveaway? (s|m|h|d|mo)",
            "What is the prize of the giveaway?"]
        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        for i in questions:
            await ctx.send(embed=discord.Embed(
                description=i,
                color=discord.Colour.red()
            ))
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(
                    description='You didn\'t answer in time, please be quicker next time!',
                    color=discord.Colour.red()
            ))
                return
            else:
                answers.append(msg.content)
        try:

            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(embed=discord.Embed(
                description=f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.",
                color=discord.Colour.red()
            ))
            return
        channel = self.bot.get_channel(c_id)

        def convert(timer):

            pos = ["s", "m", "h", "d", "mo"]
            time_dict = {"s": 1, "m": 60, "h": 60*60, "d": 3600*24, "mo": 86400*30}
            unit = timer[-1]
            if unit not in pos:
                return -1
            try:
                val = int(timer[:-1])

            except:
                return -2

            return val * time_dict[unit]

        time = convert(answers[1])
        if time == -1:
            await ctx.send(embed=discord.Embed(
                description=f"You didn't answer the time with a proper unit. Use (s|m|h|d|mo) next time!",
                color=discord.Colour.red()
            ))
            return
        elif time == -2:
            await ctx.send(embed=discord.Embed(
                description=f"The time must be an integer. Please enter an integer next time",
                color=discord.Colour.red()
            ))
            return
        prize = answers[2]

        await ctx.send(embed=discord.Embed(
                description=f"The Giveaway will be in {channel.mention} and will last {answers[1]}!",
                color=discord.Colour.green()
            ))

        embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description='**prize:** {}\n**Ends At:** {}\n**Host By:** {}'.format(prize, answers[1], ctx.author.mention))
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        my_msg = await channel.send('🎉 Giveaway! 🎉', embed=embed)
        await my_msg.add_reaction("🎉")
        await asyncio.sleep(time)
        new_msg = await channel.fetch_message(my_msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        winner = random.choice(users)

        embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description="**prize:** {}\n**Host By:** {}\n**winner:** {}".format(
                prize,
                ctx.author.mention,
                winner.mention))
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await my_msg.edit(embed=embed)
        await channel.send(embed=discord.Embed(
                description=f"the winner is {winner.mention} Won in **{prize}**!",
                color=discord.Colour.red()
            ))

    @commands.has_permissions(administrator=True)
    @giveaway_create.error
    async def giveaway_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                description="🙄 I don't have permissions",
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description="🙄 You don't have permissions",
                color=discord.Colour.red()
            ))
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help='to re-winner in giveaway')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def reroll(self, ctx, channel: discord.TextChannel, message_id: int):
        try:
            new_msg = await channel.fetch_message(message_id)

        except:
            await ctx.send(embed=discord.Embed(
                description="The id was entered incorrectly.",
                color=discord.Colour.red()
            ))
            return
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        winner = random.choice(users)
        await channel.send(embed=discord.Embed(
                description=f"the winner is {winner.mention}.!",
                color=discord.Colour.green()
            ))

    @commands.has_permissions(administrator=True)
    @reroll.error
    async def roll_winner_error(self, ctx, error):
        prefix = self.cr.execute("SELECT prefix FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description='Used: `{}reroll <#channel> id_message`'.format(prefix.fetchone()[0]),
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description="🙄 You don't have permissions",
                color=discord.Colour.red()
            ))
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(name='gstart', help='to made giveaway quick')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def giveaway_start(self, ctx, time, *, prize: str):
        await ctx.message.delete()

        def convert(time):
            pos = ["s", "m", "h", "d", "mo"]
            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24, "mo": 86400*30}
            unit = time[-1]
            if unit not in pos:
                return -1
            try:
                val = int(time[:-1])
            except:
                return -2
            return val * time_dict[unit]

        time1 = convert(time)
        embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description='**prize:** {}\n**Ends At:** {}\n**Host By:** {}'.format(prize, time, ctx.author.mention))
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        my_msg = await ctx.send('🎉 Giveaway! 🎉', embed=embed)
        await my_msg.add_reaction("🎉")

        await asyncio.sleep(time1)

        new_msg = await ctx.channel.fetch_message(my_msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        winner = random.choice(users)
        embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description='**prize:** {}\n**Host By:** {}\n**winner:** {}'.format(
                prize,
                ctx.author.mention,
                winner.mention))
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await my_msg.edit(embed=embed)
        await ctx.send(embed=discord.Embed(
                description=f"the winner is {winner.mention} won in **{prize}**!",
                color=discord.Colour.green()
            ))

    @commands.has_permissions(administrator=True)
    @giveaway_start.error
    async def giveaway_start_error(self, ctx, error):
        prefix = self.cr.execute("SELECT prefix FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description='**Used:** `{}gstart Time prize`\n**Type:** giveaway'.format(prefix.fetchone()[0]),
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                description="🙄 I don't have permissions",
                color=discord.Colour.red()
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description="🙄 You don't have permissions",
                color=discord.Colour.red()
            ))
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass


def setup(bot):
    bot.add_cog(Giveaway(bot))
