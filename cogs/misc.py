import discord
import time
from discord.ext import commands


class MiscCog(commands.Cog, name='Misc'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pfp'], name='avi', help='Get the avatar URL of the tagged user(s), or your own avatar')
    async def avatar(self, ctx, user: discord.User = ''):
        if not user:
            user = ctx.author
            uid = str(ctx.author.id)
        else:
            uid = str(user.id)
        author = ctx.message.author
        pfp = author.avatar_url
        embed = discord.Embed()
        embed.set_image(url=pfp)
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)
        await ctx.send(embed=embed)

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.


def setup(bot):
    bot.add_cog(MiscCog(bot))
