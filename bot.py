import discord
from datetime import date
from datetime import datetime
import asyncio
from discord.ext import commands
from numpy import random
import youtube_dl

TOKEN = ''

client = commands.Bot(command_prefix='/')

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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.25):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Tocando a tu hermana y tocando: {}'.format(player.title))

    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()

    @stop.before_invoke
    @play.before_invoke
    @join.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("No tas en un canal de voz maestro")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


@client.event
async def on_ready():
    print('Entre {0} ({0.id}) nadie se dio cuenta'.format(client.user))
    await client.change_presence(activity=discord.Game('Manosear a tu hermana'))
    print('Listorti')


class commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command()
    async def puto(self, ctx):
        await ctx.send('el que escribe :v')

    @commands.command()
    async def viernes(self, ctx):
        today = date.today()
        if (today.weekday() == 4): 
            await ctx.send('VIERNESS DE LA JUNGLE HIJO DE REMIL!!!')
            #await Music.play(self,ctx,'https://www.youtube.com/watch?v=OKeBuIsJl-A')
        else:
            await ctx.send('NO ES VIERNES CAPO, ESPERÁ UN TOQUE')
            """poner la musikita pum"""
    @commands.command()
    async def macaco(self, ctx, *, question):
        responses = ['si',
                    'no',
                    'no jodas',
                    'estoy cagando',
                    'Anda a la cancha bobo',
                    'definitivamente',
                    'definitivamente no',
                    'tenes razon',
                    'sopa do macaco',
                    'no te escucho mati',
                    'Dale Bokitaaaaa',
                    'bamo newveeeeeeeeel']
        await ctx.send(f'{random.choice(responses)}')
pass

@client.listen()
async def on_message(message):
    if "pone musica" in message.content.lower():
        await message.channel.send('Yo si se ponerla, no como vos salu2')
        await client.process_commands(message)

@client.listen()
async def on_message(message):
    if "me escuchan?" in message.content.lower():
        await message.channel.send('no bro. Sorry')
        await client.process_commands(message)

@client.listen()
async def on_message(message):
    if "estan?" in message.content.lower():
        await message.channel.send('No les rompas las pelotas, no te quieren')
        await client.process_commands(message)

client.add_cog(Music(client))
client.add_cog(commands(client))

client.run(TOKEN)