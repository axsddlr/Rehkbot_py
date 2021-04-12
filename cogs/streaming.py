import discord
import time
import sys
import psutil
import os
import datetime
from discord.ext import commands
from discord.ext.commands import Cog


class Streaming(Cog, name="Streaming"):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_update(self, before, after):
        activity_type = None
        streaming_role = after.guild.get_role(801934675123240960)
        try:
            activity_type = after.activity.type
        except:
            pass

        if not (activity_type is discord.ActivityType.streaming):
            # User is doing something other than streaming
            if streaming_role in after.roles:
                print(f"{after.display_name} has stopped streaming")
                await after.remove_roles(streaming_role)
        else:
            if streaming_role not in after.roles:
                # If they don't have the role, give it to them
                # If they have it, we already know they're streaming so we don't need to do anything
                print(f"{after.display_name} has started streaming")
                await after.add_roles(streaming_role)


def setup(bot):
    bot.add_cog(Streaming(bot))
