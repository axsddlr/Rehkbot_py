import discord
from discord.commands import slash_command
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.commands import Option  #Importing the packages
import datetime

from utils.utils import cfg

guilds = [cfg["GUILD_ID"]]


class ModeratorCog(commands.Cog, name="Moderator"):
    def __init__(self, bot):
        self.bot = bot

    # clear /prune command

    @slash_command(
        name="purge",
        guild_ids=guilds,
    )
    @has_permissions(ban_members=True, kick_members=True)
    async def clear(self, ctx, amount=None):
        if amount is None:
            await ctx.channel.purge(limit=5 + 1)
        elif amount == "all":
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=int(amount) + 1)

    # MUTE MEMBERS

    @slash_command(guild_ids=guilds)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Option(discord.Member)):

        await member.kick(
            reason=None)  # kick th member with no reason. you can add another option with "str" as the first param
        await ctx.respond("Done.")

    @slash_command(guild_ids=guilds)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: Option(discord.Member)):

        await member.ban(reason=None, delete_message_days=0)  # ban and dont delete any messages
        await ctx.respond("Done.")

    @commands.command()  # Because unban doesnt work with slash commands
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member):

        await member.unban(member, reason=None)
        await ctx.respond("Done.")

    @slash_command(guild_ids=guilds)
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: Option(discord.Member)):
        muted_role = ctx.guild.get_role(1234567890)  # get the muted role with ID

        await member.add_roles(muted_role)  # add the mute role

        await ctx.respond("The member has been muted")

    @slash_command(guild_ids=guilds)
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: Option(discord.Member)):
        muted_role = ctx.guild.get_role(1234567890)

        await member.remove_roles(muted_role)  # remove muted role

        await ctx.respond("The member has been unmuted")

    @slash_command(guild_ids=guilds)
    async def membercount(self, ctx):
        await ctx.respond(ctx.guild.member_count)  # get guild no. of members

    @slash_command(guild_ids=guilds)
    async def timeout(self, ctx, member: Option(discord.Member), minutes: Option(int)):
        """Apply a timeout to a member"""

        duration = datetime.timedelta(minutes=minutes)
        await member.timeout_for(duration)  # timeout for the amount of time given, then remove timeout
        await ctx.reply(f"Member timed out for {minutes} minutes.")

    @slash_command(name="slowmode", hidden=True, guild_ids=guilds)
    @has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds=None):

        if seconds is None:
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.respond(f"Succesfully removed slowmode!")


        else:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.respond(f"Succesfully set slowmode to {seconds} seconds")


def setup(bot):
    bot.add_cog(ModeratorCog(bot))
