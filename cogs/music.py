import asyncio

import discord
import youtube_dl
from discord.ext import commands
from discord.ext.commands import Cog
from discord.commands import slash_command

from utils.utils import Queue
from utils.utils import cfg

guilds = [cfg["GUILD_ID"]]

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = Queue()
        self.bg_task = None

    @slash_command(
        name="join",
        guild_ids=guilds,
    )
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @slash_command(
        name="play",
        guild_ids=guilds,
    )
    async def play(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            self.queue.push(url)
            if not ctx.voice_client.is_playing():
                self.play_songs(ctx)

        await ctx.respond(f'Added to queue!')

    @slash_command(
        name="skip",
        guild_ids=guilds,
    )
    async def skip(self, ctx):
        """Skips the current song"""

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.respond('Skipped!')
            self.play_songs(ctx)

    @slash_command(
        name="volume",
        guild_ids=guilds,
    )
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.respond("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.respond(f"Changed volume to {volume}%")

    @slash_command(
        name="stop",
        guild_ids=guilds,
    )
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        self.queue.clear()
        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.respond("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")

    def play_songs(self, ctx):
        self.bg_task = self.bot.loop.create_task(self.play_songs_task(ctx))

    async def play_songs_task(self, ctx):
        if not self.queue.isEmpty():
            try:
                url = self.queue.pop()
                print(url)
                if ctx.voice_client.is_playing() or url is None:
                    return
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                print(f'[{player.title}] playing...')
                ctx.voice_client.play(player,
                                      after=lambda e: print(f'Player error: {e}') if e else self.play_songs(ctx))
                await ctx.respond(f'Now playing: {player.title}')
            except Exception as e:
                print(e)
                await ctx.respond(f'An error occured: {e}')
        else:
            print('Queue empty, stopping...')
            await ctx.respond('Queue empty, goodbye!')
            await ctx.voice_client.disconnect()


def setup(bot):
    bot.add_cog(Music(bot))