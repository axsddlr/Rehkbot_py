from discord.ext import commands
from discord.ext.commands import has_permissions


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="load", hidden=True)
    @has_permissions(manage_guild=True)
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except commands.ExtensionError:
            await ctx.send("**`ERROR:`**")
        else:
            await ctx.send("**`SUCCESS`**")

    @commands.command(name="unload", hidden=True)
    @has_permissions(manage_guild=True)
    async def unload(self, ctx, *, cog: str):
        print(cog)
        try:
            self.bot.unload_extension(cog)
        except commands.ExtensionError:
            await ctx.send("**`ERROR:`**")
        else:
            await ctx.send("**`SUCCESS`**")

    @commands.command(name="reload", hidden=True)
    @has_permissions(manage_guild=True)
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except commands.ExtensionError:
            await ctx.send("**`ERROR:`**")
        else:
            await ctx.send("**`SUCCESS`**")

    @commands.command(name="shards", hidden=True)
    @has_permissions(manage_guild=True)
    async def getShards(self, ctx):
        await ctx.send("Shards: " + str(self.bot.shard_count))


def setup(bot):
    bot.add_cog(Owner(bot))
