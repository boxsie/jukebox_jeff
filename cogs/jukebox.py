import os
import sys
import asyncio
import discord
import shutil

from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
from utils.get_channel import get_channel_from_ctx

YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist':'True'}
TMP_FOLDER = 'tmp'

class Jukebox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='oi', help='Summons Jeff to your current channel')
    async def summon(self, ctx):
        try:
            channel = get_channel_from_ctx(bot=self.bot, ctx=ctx)
            print(f'Moving to {channel.name}')
            await self.bot.voice.join_voice_channel(channel=channel)
        except Exception as e:
            print(e)
            await ctx.message.author.send('Failed to move to channel')


    @commands.command(name='stream', help='Get Jeff to play those funky sounds')
    async def stream(self, ctx, source):
        try:
            print(f'Play audio request from {ctx.message.author} for {source}')
            yt_url, yt_title = await self._get_yt_info(source)
            channel = get_channel_from_ctx(bot=self.bot, ctx=ctx)
            await self.bot.voice.play(channel=channel, source=yt_url, title=yt_title)
        except Exception as e:
            print(e)
            await ctx.message.author.send(f'Failed to play \`{source}\`')


    @commands.command(name='stop', help='Shut up Jeff')
    async def stop(self, ctx):
        try:
            print(f'Stop audio request from {ctx.message.author}')
            await self.bot.voice.stop()
        except Exception as e:
            print(e)
            await ctx.message.author.send(f'Failed to stop')


    @commands.command(name='now', help='What tunes is Jeff currently spinning?')
    async def now_playing(self, ctx):
        try:
            playing = self.bot.voice.now_playing
            if playing:
                await ctx.send(f"I'm listening to the sweet sounds of...\n**{playing['title']}**")
            else:
                await ctx.send('I\'m aint listening to shit bruv... woof')
        except Exception as e:
            print(e)
            await ctx.message.author.send('Failed to move to channel')


    @commands.command(name='download', help='Download audio from YouTube')
    async def download(self, ctx, url):
        try:
            print(f'YouTube download request from {ctx.message.author}')
            audio_url, title = await self._get_yt_info(url)
            opts = YDL_OPTIONS
            filename = f'{title}.mp3'
            opts['outtmpl'] = os.path.join(TMP_FOLDER, filename)

            if os.path.exists(TMP_FOLDER):
                os.makedirs(TMP_FOLDER)

            with YoutubeDL(opts) as ydl:
                ydl.download([audio_url])

            await ctx.send(file=discord.File(opts['outtmpl']))
        except Exception as e:
            print(e)
            await ctx.message.author.send(f'Failed to download YouTube audo `{url}`')

        shutil.rmtree(TMP_FOLDER)


    async def _get_yt_info(self, url):
        async def _get_info(url):
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)

            audio_url = info['formats'][0]['url']
            title = info['title']

            return audio_url, title

        return await self.bot.loop.create_task(_get_info(url))