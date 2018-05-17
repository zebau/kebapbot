import random
import aiohttp
import discord
import asyncio
import os
from bs4 import BeautifulSoup
from exp import *
from os import listdir
from os.path import isfile, join
from mutagen.mp3 import MP3
from discord.ext import commands


bot = commands.Bot(command_prefix=commands.when_mentioned_or('?'), description='sounds bois')


async def music(ctx, path):
    try:
        channel = ctx.message.author.voice_channel
        server = ctx.message.server
        if channel is None:
            await bot.send_message(ctx.message.channel, "Schau dasd in an Voice Channel kimst!")
            return False
        voice = await bot.join_voice_channel(channel)
        player = voice.create_ffmpeg_player(path)
        player.start()
        counter = 0
        duration = MP3(path).info.length
        while not counter >= duration:
            await asyncio.sleep(1)
            counter = counter + 1
        await bot.voice_client_in(server).disconnect()
    except Exception as exc:
        await bot.send_message(discord.Object(id='418814283036491776'), "Error: ```{ttt}```".format(ttt=exc))


@bot.command(pass_context=True)
async def speim(ctx):
    await music(ctx, "./audio/speim.mp3")

@bot.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    await bot.change_presence(game=discord.Game(name='with Kebaps'))

bot.run("")