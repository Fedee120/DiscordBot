import discord
from datetime import date
from datetime import datetime
from discord.ext import commands
from numpy import random
import youtube_dl

bot = commands.Bot(command_prefix='/')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')
pass

bot.run('NzA1MjM3Nzk5NTkwNDI4NzYz.XqsPDg.GP7FOPjNzEGJSuKPKmAsFXiV7gI')