import discord
import random
import time
from discord.ext import commands


class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member):
        """Says when a member joined."""
        await ctx.send(f'{member.display_name} joined on {member.joined_at}')

    @commands.command(name='ping', help='check if bot is working')
    @commands.has_any_role(236267540777533440)
    async def ping(self, ctx):
        await ctx.send(f'My Latency : {round(self.bot.latency*1000)}ms')

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
        muted_role = ctx.guild.get_role(DISCORD_bot_ID)

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
    bot.add_cog(CommandsCog(bot))
