import discord
import random
import os
import time
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot_id = os.getenv('DISCORD_BOT_ID')


class ModeratorCog(commands.Cog, name='Moderator'):
    def __init__(self, bot):
        self.bot = bot


# clear /prune command

    @commands.command(aliases=['prune'])
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def clear(self, ctx, amount=None):
        if amount is None:
            await ctx.channel.purge(limit=5)
        elif amount == "all":
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=int(amount))


# MUTE MEMBERS

    @commands.command(aliases=['m'])
    @commands.has_permissions(kick_members=True)
    async def mute(ctx, member: discord.Member):
        muted_role = ctx.guild.get_role(bot_id)

        await member.add_roles(muted_role)
        await ctx.send(f'{ member.mention } has been muted')

# KICK MEMBERS

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason='no reason provided :/'):
        try:
            await member.send(f'{ member.name } has been kicked from this community, because { reason }')
        except:
            await ctx.send(f'oops! it seems like { member.name } has closed their dms')
            await member.kick(reason=reason)

# BAN MEMBERS

    @commands.command(aliases=['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason='no reason provided :/'):
        try:
            await member.send(f'{ member.name } has been banned from this community, because { reason }')
        except:
            await ctx.send(f'oops! it seems like { member.name } has closed their dms')
            await member.ban(reason=reason)

# UNBAN MEMBERS

    @commands.command(aliases=['ub'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: discord.Member):
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split('#')

        for banned_entry in banned_users:
            user = banned_entry.user

        if (user.name, user.discrimiator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            await ctx.send(f'{ member_name } has been unbanned!')
            return

        await ctx.send(f"{ member } wasn't found :(")

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.


def setup(bot):
    bot.add_cog(ModeratorCog(bot))
