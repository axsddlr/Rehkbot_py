

from dotenv import load_dotenv
from discord.ext import commands, tasks
import urllib.request
import requests
import discord
import json
import aiohttp
import re
import sys
import os
import asyncio
import random
import ffmpeg
from ffprobe import *
import youtube_dl
from youtubesearchpython import *

sys.path.insert(1, './valorant')
import RiotAuth as rs
import resources as res
from urllib.parse import urlparse


ydl_opts = {
    # names downloaded file test.mp3 and places it in desired directory
    'outtmpl': './test.mp3',
    'format': 'bestaudio/best',  # quality settings
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')
# bot.remove_command("help")

# os.system('python music.py')


# Valorant stats processor
async def process_stats(author, num_matches=3):

    with open('info.json', 'r') as f:
        users = json.load(f)

    username = users['admin']['username']
    password = users['admin']['password']
    user_id = users[author]['user_id']
    _, headers = await rs.run(username, password)
    after, diff, rank_nums, maps, arrows, start_times = await rs.get_stats(user_id, headers, num_matches)
    rank_num = rank_nums[0]
    stats = zip(diff, maps, arrows, start_times)
    rank = res.ranks[str(rank_num)]
    RP = after[0]
    ELO = (rank_num * 100) - 300 + RP

    return stats, rank_num, rank, RP, ELO

# Twitch URL
my_twitch_url = "https://twitch.tv/rehkloos"

'''
EVENTS
1. Check whether bot is ready/online
2. Delete messages with "bad words"
3. Return on command error
'''

# set watch status for bot


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Rehkloos", url=my_twitch_url))

# automatic moderation
f1 = open('./assets/bad_words.txt', 'r')
bw = f1.readlines()

bad_words = []
for i in range(len(bw)):
    bad_words.append(bw[i].replace("\n", ""))


@bot.event
async def on_message(msg):
    for word in bad_words:
        if word in msg.content.lower():
            await msg.delete()

    await bot.process_commands(msg)
    


# command error


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("oops! you can't do that")
        await ctx.message.delete()

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("seems like you forgot to enter the extra information required 😞 pls try again")
        await ctx.message.delete()

    else:
        raise error


# COMMANDS

# ping
@bot.command(name='ping', help='check if bot is working')
@commands.has_any_role(236267540777533440)
async def ping(ctx):
    await ctx.send("pong.")

# Music


@bot.command()
async def play(ctx, *, mess):  # play is the argument used after the user types the prefix
    # makes the channel varible = to the channel name that the person who used the command is in
    channel = ctx.author.voice.channel
    # deletes old music file before new one is downloaded by youtube_dl
    os.remove("test.mp3")
    # takes mess(user input from discord) and searched youtube and returns a messed up dictonary
    videosSearch = VideosSearch(mess, limit=1, language='en', region='US')
    # makes the output of the search a dict
    results = videosSearch.result(mode=ResultMode.dict)
    # remove the messed up parts of the returned dict form the search results
    unfinishedlink = str(results['result']).strip('[]')
    # makes the varible unfinisedlink back into a dict (could technicly be unsafe)
    link = eval(unfinishedlink)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:  # youtube_dl stuff
        # the [link['link]] returns a url that is stored in the dict link (can be confusing needs updated)
        ydl.download([link['link']])
    # varible used to store the song name not needed as you could just put it directly into the vc.play...
    song = "test.mp3"
    vc = await channel.connect()  # define vc for use in the next line
    vc.play(discord.FFmpegPCMAudio(song), after=lambda e: print(
        'done', e))  # uses ffmpeg to play "song" aka test.mp3


# '''
# CUSTOM HELP COMMAND
# - Changing the Default Command
# '''

# CUSTOM HELP COMMAND
# @bot.group(invoke_without_command=True)
# async def help(ctx):
#     embed = discord.Embed(
#         title='**help**',
#         description='use ``bot help <command>`` for more information',
#         color=discord.Colour(0x53AFF0)
#     )
#     embed.add_field(name="introduction", value="hello, whois, rules", inline=False)
#     embed.add_field(name="moderation", value="clear, mute, kick, ban, unban", inline=False)
#     embed.add_field(name="memes", value="reddit, starter", inline=False)
#     await ctx.send(embed=embed)

# # hello
# @help.command()
# async def hello(ctx):
#     embed = discord.Embed(
#         title="``hello``",
#         description="an introduction to meme-a-tron-2000",
#         color=discord.Colour(0x53AFF0))
#     embed.add_field(
#         name="*syntax*",
#         value="bot hello"
#         )
#     await ctx.send(embed=embed)

# # whois
# @help.command()
# @commands.has_permissions(kick_members=True)
# async def whois(ctx, member: discord.Member):
#     embed = discord.Embed(
#         title="``whois``",
#         description="find out more about a member",
#         color=discord.Colour(0x53AFF0))
#     embed.add_field(
#         name="*syntax*",
#         value="bot whois @<member>"
#         )
#     await ctx.send(embed=embed)


'''
CUSTOM COMMANDS
'''

# avatar


@bot.command(aliases=['pfp'], name='avi', help='Get the avatar URL of the tagged user(s), or your own avatar')
async def avatar(ctx, user: discord.User = ''):
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


'''
Games
'''
# the 8ball command


@bot.command(aliases=['8ball'])
async def eightball(ctx, *, arg):
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


# Roll Dice
@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
            ]
    await ctx.send(','.join(dice))

'''
MODERATION COMMANDS
1. Clear Messages
2. Mute Members
3. Kick Members
4. Ban Members
5. Unban Members
'''

# clear /prune command


@bot.command(aliases=['prune'])
@commands.has_permissions(ban_members=True, kick_members=True)
async def clear(ctx, amount=None):
    if amount is None:
        await ctx.channel.purge(limit=5)
    elif amount == "all":
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=int(amount))


# MUTE MEMBERS
@bot.command(aliases=['m'])
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member):
    muted_role = ctx.guild.get_role(DISCORD_bot_ID)

    await member.add_roles(muted_role)
    await ctx.send(f'{ member.mention } has been muted')

# KICK MEMBERS


@bot.command(aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason='no reason provided :/'):
    try:
        await member.send(f'{ member.name } has been kicked from this community, because { reason }')
    except:
        await ctx.send(f'oops! it seems like { member.name } has closed their dms')
    await member.kick(reason=reason)

# BAN MEMBERS


@bot.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason='no reason provided :/'):
    try:
        await member.send(f'{ member.name } has been banned from this community, because { reason }')
    except:
        await ctx.send(f'oops! it seems like { member.name } has closed their dms')
    await member.ban(reason=reason)

# UNBAN MEMBERS


@bot.command(aliases=['ub'])
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member: discord.Member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name, user.discrimiator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            await ctx.send(f'{ member_name } has been unbanned!')
            return

    await ctx.send(f"{ member } wasn't found :(")


'''
VALORANT
'''


@bot.command()
# Only server Owner can use this command via COPY ID
@commands.has_any_role(236267540777533440)
async def login(ctx, username: str = '', password: str = ''):

    try:
        author = str(ctx.author.id)
        with open('info.json', 'r') as f:
            users = json.load(f)

        user_id, _ = await rs.run(username, password)

        if not author in users:
            users[author] = {}
            users[author]['user_id'] = user_id
            with open('info.json', 'w') as f:
                json.dump(users, f, indent=4)

            await ctx.send('Login Successful.')
        else:
            await ctx.send('You are already logged in.')

    except Exception as e:
        await ctx.send("Invalid Login.")


@bot.command()
@commands.has_any_role(236267540777533440)
async def logout(ctx):

    author = str(ctx.author.id)
    with open('info.json', 'r') as f:
        users = json.load(f)

    if author in users:
        del users[author]
        with open('info.json', 'w') as f:
            json.dump(users, f, indent=4)

        await ctx.send('You have logged out.')
    else:
        await ctx.send('You are not logged in.')


@bot.command()
async def profile(ctx, user: discord.User = ''):

    if not user:
        user = ctx.author
        uid = str(ctx.author.id)
    else:
        uid = str(user.id)

    # num_matches = min if num_matches < min else max if num_matches > max else num_matches
    try:
        stats, rank_num, rank, RP, ELO = await process_stats(uid, 3)
    except:
        await ctx.send('User is not logged in or has not played enough recent competitve games')
        return

    description = f'**{RP} RP** | **{ELO} ELO**'
    embed = discord.Embed(title=rank, description=description)

    embed.set_author(name=user.display_name, icon_url=user.avatar_url)

    embed.set_thumbnail(
        url=f'https://github.com/RumbleMike/ValorantStreamOverlay/blob/main/Resources/TX_CompetitiveTier_Large_{rank_num}.png?raw=true')
    for num, mmap, arrow, start_time in stats:
        result = '🟢' if num > 0 else '🔴'
        stat = f'+{num} RP' if num > 0 else f'{num} RP'
        match_map = res.maps[mmap]
        movement = res.movements[arrow]
        embed.add_field(name=f'{result} {match_map} ∙ {start_time}',
                        value=f'{movement} {stat}', inline=False)

    await ctx.send(embed=embed)

if __name__ == '__main__':
    bot.run(TOKEN)
